const { Sequelize, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');

const sequelize = new Sequelize(process.env.DATABASE_URL, {
    dialect: 'postgres',
    logging: false,
});

// User model
const User = sequelize.define('User', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
        validate: { len: [3, 32] }
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
        validate: { isEmail: true }
    },
    progress: {
        type: DataTypes.JSONB,
        defaultValue: {}
    }
}, {
    timestamps: true,
    hooks: {
        beforeCreate: async (user) => {
            try {
                user.password = await bcrypt.hash(user.password, 12); // Stronger salt
            } catch (err) {
                throw new Error('Password hashing failed');
            }
        },
        beforeUpdate: async (user) => {
            if (user.changed('password')) {
                try {
                    user.password = await bcrypt.hash(user.password, 12);
                } catch (err) {
                    throw new Error('Password hashing failed');
                }
            }
        }
    }
});

// Tutorial model
const Tutorial = sequelize.define('Tutorial', {
    title: {
        type: DataTypes.STRING,
        allowNull: false,
        validate: { notEmpty: true }
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false,
        validate: { notEmpty: true }
    },
    completed: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    }
}, { timestamps: true });

// Glossary model
const Glossary = sequelize.define('Glossary', {
    term: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
        validate: { notEmpty: true }
    },
    definition: {
        type: DataTypes.TEXT,
        allowNull: false,
        validate: { notEmpty: true }
    },
    tags: {
        type: DataTypes.ARRAY(DataTypes.STRING),
        defaultValue: []
    }
}, { timestamps: true });

// Associations with cascade delete
User.hasMany(Tutorial, { foreignKey: 'userId', onDelete: 'CASCADE' });
Tutorial.belongsTo(User, { foreignKey: 'userId' });

User.hasMany(Glossary, { foreignKey: 'userId', onDelete: 'CASCADE' });
Glossary.belongsTo(User, { foreignKey: 'userId' });

module.exports = {
    User,
    Tutorial,
    Glossary,
    sequelize
};