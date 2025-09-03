# PowerShell script to build Sphinx documentation
# Usage: .\build-docs.ps1 [format] [options]
# Format options: html, pdf, epub, latex (default: html)

param(
    [string]$Format = "html",
    [switch]$Clean = $false,
    [switch]$Open = $false,
    [switch]$Watch = $false,
    [switch]$Help = $false
)

# Set variables
$DocsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $DocsDir
$BuildDir = Join-Path $DocsDir "_build"
$PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if ($Help) {
    Write-Host "Sphinx Documentation Builder"
    Write-Host "Usage: .\build-docs.ps1 [format] [options]"
    Write-Host ""
    Write-Host "Formats:"
    Write-Host "  html     Build HTML documentation (default)"
    Write-Host "  pdf      Build PDF documentation"
    Write-Host "  epub     Build EPUB documentation"
    Write-Host "  latex    Build LaTeX documentation"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Clean   Clean build directory before building"
    Write-Host "  -Open    Open documentation in browser after building"
    Write-Host "  -Watch   Watch for changes and rebuild automatically"
    Write-Host "  -Help    Show this help message"
    exit 0
}

# Change to docs directory
Set-Location $DocsDir

Write-Host "Building Sphinx documentation..." -ForegroundColor Green
Write-Host "Project root: $ProjectRoot"
Write-Host "Docs directory: $DocsDir"
Write-Host "Format: $Format"

# Clean build directory if requested
if ($Clean) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    if (Test-Path $BuildDir) {
        Remove-Item $BuildDir -Recurse -Force
    }
}

# Ensure Python virtual environment is available
if (-not (Test-Path $PythonPath)) {
    Write-Host "Python virtual environment not found at: $PythonPath" -ForegroundColor Red
    Write-Host "Please ensure the virtual environment is set up correctly." -ForegroundColor Red
    exit 1
}

# Set environment variable for Python path
$env:PYTHONPATH = Join-Path $ProjectRoot "src"

try {
    if ($Watch) {
        Write-Host "Starting watch mode for automatic rebuilding..." -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop watching."
        
        # Install sphinx-autobuild if not available
        & $PythonPath -m pip install sphinx-autobuild
        
        # Start watching
        & $PythonPath -m sphinx_autobuild . "_build/$Format" --port 8000 --host 127.0.0.1
    }
    else {
        # Build documentation
        Write-Host "Running sphinx-build..." -ForegroundColor Blue
        & $PythonPath -m sphinx -b $Format . "_build/$Format"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Documentation built successfully!" -ForegroundColor Green
            Write-Host "Output directory: $(Join-Path $BuildDir $Format)" -ForegroundColor Cyan
            
            # Open in browser if requested
            if ($Open -and $Format -eq "html") {
                $IndexFile = Join-Path $BuildDir "$Format\index.html"
                if (Test-Path $IndexFile) {
                    Write-Host "Opening documentation in browser..." -ForegroundColor Blue
                    Start-Process $IndexFile
                }
            }
        }
        else {
            Write-Host "Documentation build failed!" -ForegroundColor Red
            exit $LASTEXITCODE
        }
    }
}
catch {
    Write-Host "Error building documentation: $_" -ForegroundColor Red
    exit 1
}
