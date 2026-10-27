---
url: https://chatgpt.com/c/6ae0685d-d780-83e8-9eef-fbc20fa22919
note: SDD Manager - docs/demo/hello_world/prompts/Autodoc 3in1 Baseline.md
---

> [!IMPORTANT]
>
> **Historical exploration transcript.** This document is retained for provenance and is not authoritative for current behavior or agent instructions.

## Seed Prompt

> [!NOTE] Prompt
>
> Help me develop the following project using $sdd-manager in autodoc mode.
> 
> ### Project repo and credentials
> 
> GitHub repository: https://github.com/{OWNER}/{REPO}
> 
> GitHub token: {FINE_GRAINED_GH_TOKEN}
> 
> ### Versioning and releases
> 
> Manage the project's versioning, choosing an appropriate initial version and increasing it to reflect delivered changes. After each implementation phase is completed, verified and integrated, create and publish a new GitHub release with the corresponding version tag and release notes.
> 
> Deliver the browser app, Windows Electron app and browser extensions in separate phases, in that order, with a separate release after each delivery platform is added. Treat the Chromium and Firefox extensions as one delivery platform: deliver both in the same phase and release.
> 
> Each GitHub release must include the installable or deployable artifacts for every platform delivered by that phase: the browser app build, Windows Electron package, and Chromium and Firefox extension packages, as applicable. Include installation instructions and clearly distinguish development packages from signed or store-distributed packages. Do not claim a platform delivered until its packaged artifact has been verified.
> 
> ### Project
> 
> Treat this description as the complete target scope. Deliver the baseline first, then add the delivery platforms below through bounded phases that each deliver a usable application on the added platform.
> 
> #### Baseline MVP Scope
> 
> Display the message "Hello World" and a group of three vertically stacked radio buttons labeled "red", "blue" and "green". Selecting a radio button immediately changes the message's text color to the selected color, without a separate apply action. Exactly one radio button is selected at a time; initially select "red" and display the message in red.
> 
> #### Platforms
> 
> ##### Browser app - baseline delivery
> 
> Initially deliver a browser app. Design application logic and UI for reuse across future delivery platforms, including a Windows Electron desktop app and sidebar extensions for desktop Chromium and Firefox, keeping platform-specific code separate so that most of the codebase can be shared.
> 
> ##### Windows Electron delivery
> 
> Add an Electron packaged app for Windows as a second delivery platform after the browser baseline is implemented and verified. Keep the application usable in a browser, bundle all required desktop runtime assets, and require no separate Node.js installation or development server. Share application logic and UI between browser and desktop versions, adapting platform-specific behavior as needed. Include the Windows package alongside the browser build in applicable GitHub releases.
> 
> ##### Browser extension delivery
> 
> Add sidebar extensions for desktop Chromium and Firefox together as the final delivery platform, after Windows Electron delivery. Keep the browser and desktop versions available and share application logic and UI across all versions. Bundle all required extension runtime assets; users must not need a separate Node.js installation, local development server or backend. Include both extension packages in applicable GitHub releases.
> 
> Adapt the layout to a narrow, resizable sidebar while retaining access to the same in-scope capabilities. Apply platform-specific persistence, file-operation and lifecycle adaptations only when the corresponding capability is in scope. Use extension-local storage where persistent data is required; preserve session-only behavior where specified. During document preparation, resolve panel closing and reopening behavior and, where applicable, adaptations of cookie/URL configuration and file import/export requirements. These conditional instructions do not introduce additional application capabilities.
> 
> ### Design clarification
> 
> During preparation, resolve important interactions and boundary cases across the requested platforms, including initial state, input behavior, layout constraints and application lifecycle. Address persistence and file operations only where required by the application scope. Surface decisions that materially affect behavior before implementation.
