## UV workflow

#### Add a new package → automatically updates pyproject.toml + uv.lock

`uv add pandas`

#### Remove a package

`uv remove pandas`

#### Someone else (or future you) clones the repo

`git clone …`  
`cd agents`  
`uv sync` # ← 5–10 seconds and 100% identical environment
