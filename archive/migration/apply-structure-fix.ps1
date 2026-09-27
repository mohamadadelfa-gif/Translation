param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath
)

$ErrorActionPreference = 'Stop'
throw 'Retired migration helper: retained for audit history only. Its force-copy operations can overwrite current policy and glossary decisions. Review the active project files directly; do not run this bundle.'
$bundle = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path $RepoPath).Path

if (-not (Test-Path (Join-Path $repo '.git'))) {
    throw "Not a Git repository: $repo"
}

$replace = @(
    'AGENTS.md',
    'MENTOR_WORKFLOW.md',
    'README.md',
    'drafts/README.md',
    'approved-translations/README.md',
    'translation-references/GLOSSARY.md'
)

foreach ($rel in $replace) {
    $src = Join-Path $bundle $rel
    $dst = Join-Path $repo $rel
    $parent = Split-Path -Parent $dst
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    Copy-Item -Force $src $dst
}

$registerPath = Join-Path $repo 'translation-references/SOURCE-REGISTER.md'
$register = Get-Content -Raw -Encoding UTF8 $registerPath
$old = 'The mentor.md plan and current project instructions guide pedagogy rather than supply lexical evidence.'
$new = '`MENTOR_WORKFLOW.md` and the current project instructions guide pedagogy rather than supply lexical evidence.'
if ($register.Contains($old)) {
    $register = $register.Replace($old, $new)
    Set-Content -Encoding UTF8 -NoNewline $registerPath $register
} else {
    Write-Warning 'SOURCE-REGISTER.md: expected mentor.md sentence not found; review manually.'
}

$startPath = Join-Path $repo 'translation-preparation/START-HERE.md'
$start = Get-Content -Raw -Encoding UTF8 $startPath
$heading = "## How to use this structure`n"
$insert = "`nThe ``Cxx-Sxx`` identifiers below are structural translation units, not fixed 300-word mentoring sessions. For day-to-day practice, divide the current unit into coherent ~250–350-word practice chunks identified as ``Cxx-Sxx-P01``, ``P02``, and so on. Chunk boundaries are workflow aids and must not alter the source text or original section boundaries.`n"
if ($start.Contains($heading) -and -not $start.Contains('structural translation units, not fixed 300-word mentoring sessions')) {
    $start = $start.Replace($heading, $heading + $insert)
    Set-Content -Encoding UTF8 -NoNewline $startPath $start
} elseif ($start.Contains('structural translation units, not fixed 300-word mentoring sessions')) {
    Write-Host 'START-HERE.md hierarchy note already present.'
} else {
    Write-Warning 'START-HERE.md: expected heading not found; review manually.'
}

Write-Host "`nStructural files applied. Review the diff before committing:`n"
Push-Location $repo
try {
    git diff -- AGENTS.md MENTOR_WORKFLOW.md README.md drafts/README.md approved-translations/README.md translation-references/GLOSSARY.md translation-references/SOURCE-REGISTER.md translation-preparation/START-HERE.md
} finally {
    Pop-Location
}
