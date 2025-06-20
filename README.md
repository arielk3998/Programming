# Programming Repository

This repository contains a collection of programming projects and utilities, organized by language and purpose.  
It is designed for easy navigation, reuse, and extension of code across different technologies.

---

## Directory Structure

- **Python/**
  - **Blender/**  
    Blender automation scripts, scene generators, and global utility functions for 3D graphics and animation.
    - `Automation/`  
      High-level automation scripts (e.g., `main_AutomateGraphicDesignTools.py`) that orchestrate scene creation and rendering.
    - `Blender Global Functions/`  
      Modular, reusable functions for Blender scripting (e.g., adding objects, setting up lighting, rendering, etc.).
    - `render/`  
      Output directory for rendered images and animations.
    - `Notes on how to imrove the code.md`  
      Guidelines and action plans for improving code quality and scene realism.
    - `Scene Generator Notes.md`  
      Notes and recommendations for building scene generation tools and GUIs.

- **Other Languages/**  
  Additional folders for other programming languages and projects as needed.

---

## Getting Started

1. **Browse the folders** to find scripts or utilities relevant to your needs.
2. **For Blender scripts:**
   - Ensure you are running inside Blender’s Python environment.
   - Place the `Blender Global Functions` directory in your Python path or use the provided automation scripts as templates.
   - Review and adjust parameters in the automation scripts as needed.
3. **Refer to the notes** in each folder for best practices, improvement ideas, and usage instructions.

---

## Blender Automation Example

To automate scene creation and rendering in Blender, run:

```bash
blender --background --python Python/Blender/Automation/main_AutomateGraphicDesignTools.py
```

This will:
- Clear the scene
- Add ground, donut, camera, and lighting
- Set render settings
- Bake physics
- Render the animation

---

## Contribution & Maintenance

- Contributions, suggestions, and improvements are welcome.
- Please follow best practices for code clarity, documentation, and organization.
- See `Notes on how to imrove the code.md` for ongoing improvement plans.

---

*Maintained by Ariel. For questions or feedback, please open an issue or contact
