# Group04-10.-Course-Registration-Svstem
```markdown
II. Non-functional requirements:
  1. Product requirements:
     1.1. Usability requirements:
       -Users shall do basic tasks with the program within 30 minutes.
       -Common tasks should be completed in no more than 3-4 steps.
       -The interface includes layout, buttons, colors, and messages that follow the same conventions on every screen.
     1.2. Efficiency requirements:
       a) Performance requirements:
         -The application starts within about 3–5 seconds on an ordinary computer.
         -Adding, editing, or deleting a single record responds in under 2 seconds.
         -Searching and displaying a list from a dataset takes under 3 seconds.
       b) Space requirements:
         -The application uses under 200 MB at most and needs no special hardware or graphics card.
         -Errors are logged for tracing, and no data is lost in the event of a sudden failure.
     1.3. Dependability requirements:
       -The system runs with a target error-free operation rate of ≥ 90%.
       -The system should be available throughout the day. Downtime within normal working hours shall not exceed five seconds in any one day.
       -The system should not have more than 10 errors. The time limit allowed for reporting a detailed error is 3 seconds.
     1.4. Security requirements:
       -Users shall log in with a username and password. Passwords are hashed with a salt using an algorithm such as bcrypt and are never stored in plain text.
       -Every query uses parameterized statements, and user input is never concatenated into SQL strings.
  3. Organizational requirements:
     2.1. Environmental requirements:
       -The application should run on operating systems like Windows 10/11 with low minimum hardware requirements, including a 2-core CPU, 4 GB RAM, and 2 GB of free disk space.
     2.2. Operational requirements:
       -Each user shall have their own authentication code to verify their identity when using the system.
     2.3. Development requirements:
       -Programming language: Python
       -Database management system: PostgreSQL
       -Documentation, source code, and team management: GitHub
       -Drawing DFD, Use Case, Class Diagram, and Database Schema: https://app.diagrams.net/
       -GUI design: Figma
       -Creating test cases: Excel
       -Programming IDEs: VS Code
       -Bug tracking tools: Bugzilla
       -Unit testing: pytest (Python)
       -Packaging and deployment: Docker
  5. Extenal requiments:
       -The system shall implement user privacy provisions as set out in Decree No. 13/2023/ND-CP on Personal Data Protection.
       


