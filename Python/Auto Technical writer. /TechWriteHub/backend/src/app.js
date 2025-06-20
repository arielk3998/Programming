const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { sequelize } = require('./models');
const userRoutes = require('./userRoutes/userRoutes');
const tutorialRoutes = require('./userRoutes/tutorialRoutes');
const glossaryRoutes = require('./userRoutes/glossaryRoutes');

dotenv.config();

if (!process.env.DATABASE_URL) {
    console.error('DATABASE_URL is not set in environment variables.');
    process.exit(1);
}

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// Health check route
app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

// Routes
app.use('/api/users', userRoutes);
app.use('/api/tutorials', tutorialRoutes);
app.use('/api/glossary', glossaryRoutes);

// Centralized error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(err.status || 500).json({ error: err.message || 'Internal Server Error' });
});

// Database connection and server start
const startServer = async () => {
    try {
        await sequelize.authenticate();
        await sequelize.sync();
        console.log('PostgreSQL connected');
        const server = app.listen(PORT, () => {
            console.log(`Server is running on http://localhost:${PORT}`);
        });

        // Graceful shutdown
        process.on('SIGINT', async () => {
            server.close(async () => {
                console.log('Server closed');
                await sequelize.close();
                console.log('PostgreSQL connection closed');
                process.exit(0);
            });
        });
    } catch (err) {
        console.error('Database connection error:', err);
        process.exit(1);
    }
};

startServer();