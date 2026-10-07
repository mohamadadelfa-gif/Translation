param(
    [string]$SourcePath = $env:ZERO_HOUR_SOURCE_MD
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($SourcePath)) {
    $SourcePath = Join-Path $projectRoot 'sources\revisiting-zero-hour-1945-structured.md'
}
if (!(Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
    throw "Source Markdown not found: $SourcePath. Pass -SourcePath or set ZERO_HOUR_SOURCE_MD."
}

$source = [IO.File]::ReadAllText($SourcePath).Replace("`r`n", "`n")

# The frozen supplied snapshot already contains earlier preparation markers.
# Strip only known project-generated markers before rebuilding the working layer.
$source = [regex]::Replace(
    $source,
    '(?m)^<!-- translation-preparation: added unit heading -->\n#### Translation unit C\d\d-S\d\d\n\n',
    ''
)
$source = [regex]::Replace(
    $source,
    '(?m)^<!-- practice-chunk: C\d\d-S\d\d-P\d\d (?:START|END)(?:; source words: \d+)? -->\n?',
    ''
)

$out = Join-Path $projectRoot 'translation-preparation'
[IO.Directory]::CreateDirectory($out) | Out-Null
$starts = [regex]::Matches($source, '(?m)^## (Introduction|German Culture at.*|From Zero Hour to High Noon:.*|Adorno.s Philosophy.*|.Where Were You.*|Divided Memory, Multiple Restorations:.*)$')
if ($starts.Count -ne 6) { throw 'Expected introduction and five essays.' }
$front = $source.Substring(0, $starts[0].Index)
$master = [Text.StringBuilder]::new()
[void]$master.Append($front)
$index = [Collections.Generic.List[string]]::new()
$index.Add('# Revisiting Zero Hour 1945 — Translation Map')
$index.Add('')
$index.Add('## How to use this structure')
$index.Add('')
$index.Add('The `Cxx-Sxx` identifiers below are structural translation units, not fixed 300-word mentoring sessions. For daily practice, divide the current unit into coherent 250–350-word chunks identified as `Cxx-Sxx-P01`, `P02`, and so on, guided primarily by paragraph and argument logic. Record each chunk''s exact source boundaries and draft/review/approval state in [PROGRESS.md](../PROGRESS.md). Sentence IDs such as `C00-S02-P03-SEN01` are optional analytical aids. These divisions must not alter the source text.')
$index.Add('')
$index.Add('1. Read the introduction and establish translation conventions and a shared glossary.')
$index.Add('2. Translate the introduction (C00), then the five essays (C01–C05) in order, one numbered unit at a time.')
$index.Add('3. Use the full chapter as context. Consult its endnotes while translating each unit; translate the endnotes after the chapter body.')
$index.Add('4. Review the complete chapter for terminology, argument, quotations, and transitions before moving on.')
$index.Add('5. Translate the front matter and review the complete volume.')
$index.Add('')
$index.Add('Chapter codes and translation-unit headings are editorial aids added for this project, not numbering or titles supplied by the authors. Original headings, text, spelling, citations, and endnotes are preserved. Units follow original sections and paragraph boundaries; word counts are approximate. Very short original sections remain intact. Boundaries in long passages are practical working divisions and can be adjusted during translation.')
$index.Add('')
$index.Add('[Complete structured source](revisiting-zero-hour-1945-structured.md) · [Front matter](front-matter.md)')
# Standalone front matter needs file links; keep the full source's anchors intact.
$frontLinkState = @{ Count = 0 }
$standaloneFront = [regex]::Replace($front, '(?m)^- (\[[^\r\n]+\])\(#[^)]+\)( — [^\r\n]+)$', {
    param($match)
    $target = 'C{0:D2}.md' -f $frontLinkState.Count
    $frontLinkState.Count++
    '- ' + $match.Groups[1].Value + '(' + $target + ')' + $match.Groups[2].Value
})
if ($frontLinkState.Count -ne 6) { throw 'Expected six chapter links in standalone front matter.' }
[IO.File]::WriteAllText((Join-Path $out 'front-matter.md'), $standaloneFront)
$unitCount = 0
for ($c = 0; $c -lt $starts.Count; $c++) {
    $start = $starts[$c].Index
    $end = if ($c + 1 -lt $starts.Count) { $starts[$c+1].Index } else { $source.Length }
    $chapter = $source.Substring($start, $end-$start)
    $code = 'C{0:D2}' -f $c
    $filename = "$code.md"
    $title = $starts[$c].Groups[1].Value
    $index.Add('')
    $label = if ($c -eq 0) { 'Introduction' } else { "Chapter $c" }
    $index.Add("## $code — $label")
    $index.Add('')
    $index.Add("[$title]($filename)")
    $index.Add('')
    $index.Add('| Unit | Original section | Approx. words |')
    $index.Add('| --- | --- | ---: |')
    $blocks = [regex]::Matches($chapter, '(?s)\S.*?(?:\n\s*\n|\z)')
    $insertions = [Collections.Generic.List[object]]::new()
    $section = 'Opening discussion'
    $words = 0
    $unit = 0
    $active = $false
    $notes = $false
    $previous = ''
    foreach ($b in $blocks) {
        $text = $b.Value.Trim()
        # This original subsection is bold in the supplied source, not a ### heading.
        if ($text -match '^### (.+)' -or $text -match '^\*\*(The Origins of the Term “Zero Hour”)\*\*$') {
            if ($active) { $index.Add("| $code-S$('{0:D2}' -f $unit) | $section | $words |") }
            $active = $false; $words = 0; $section = $Matches[1]
            if ($section -eq 'Endnotes') { $notes = $true }
            continue
        }
        if ($notes -or $text -match '^## ' -or $text -match '^\*\*[^\n]+\*\*$' -or $text -match '^\*Original printed pages' -or $text -eq '---') { continue }
        $n = [regex]::Matches($text, '\S+').Count
        $safeBoundary = $text -notmatch '^>' -and $previous -notmatch ':\s*$'
        if (!$active -or ($words -ge 1000 -and $words+$n -gt 1400 -and $safeBoundary)) {
            if ($active) { $index.Add("| $code-S$('{0:D2}' -f $unit) | $section | $words |") }
            $unit++; $unitCount++; $words = 0; $active = $true
            $id = "$code-S$('{0:D2}' -f $unit)"
            $insertions.Add(@{ Position=$b.Index; Value="<!-- translation-preparation: added unit heading -->`n#### Translation unit $id`n`n" })
        }
        $words += $n
        $previous = $text
    }
    if ($active) { $index.Add("| $code-S$('{0:D2}' -f $unit) | $section | $words |") }
    $index.Add('')
    $index.Add("Endnotes: retain with $code and consult alongside its translation units.")
    $edited = $chapter
    for ($i=$insertions.Count-1; $i -ge 0; $i--) { $edited = $edited.Insert($insertions[$i].Position, $insertions[$i].Value) }
    $restored = [regex]::Replace($edited, '<!-- translation-preparation: added unit heading -->\n#### Translation unit C\d\d-S\d\d\n\n', '')
    if ($restored -cne $chapter) { throw "Source-preservation check failed for $code" }
    [IO.File]::WriteAllText((Join-Path $out $filename), $edited)
    [void]$master.Append($edited)
}
$whole = $master.ToString()
$restoredWhole = [regex]::Replace($whole, '<!-- translation-preparation: added unit heading -->\n#### Translation unit C\d\d-S\d\d\n\n', '')
if ($restoredWhole -cne $source) { throw 'Full-source preservation check failed.' }
[IO.File]::WriteAllText((Join-Path $out 'revisiting-zero-hour-1945-structured.md'), $whole)
[IO.File]::WriteAllText((Join-Path $out 'START-HERE.md'), ($index -join "`n"))
Write-Output "Source: $SourcePath"
Write-Output "Created introduction + 5 chapters, $unitCount translation units. Verified all normalized source content preserved."
Write-Output ($index -join "`n")
