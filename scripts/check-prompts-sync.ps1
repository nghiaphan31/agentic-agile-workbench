<#
.DESCRIPTION
Vérifie la cohérence entre les System Prompts canoniques (dossier prompts/) et leurs artefacts déployés.
Génère un rapport dans docs/qa/SP-COHERENCE-YYYY-MM-DD.md.

.PARAMETER Force
Force la régénération du rapport même si les fichiers n'ont pas changé.

.EXAMPLE
PS> .\scripts\check-prompts-sync.ps1
PS> .\scripts\check-prompts-sync.ps1 -Force
#>

param (
    [switch]$Force
)

# Configuration
$PROJECT_ROOT = $PSScriptRoot.TrimEnd('\scripts')
$PROMPTS_DIR = "$PROJECT_ROOT\prompts"
$QA_DIR = "$PROJECT_ROOT\docs\qa"
$REPORT_FILE = "$QA_DIR\SP-COHERENCE-$((Get-Date).ToString('yyyy-MM-dd')).md"

# Fichiers à vérifier (SP-XXX -> Artefact)
$SP_MAPPING = @{
    "SP-001-ollama-modelfile-system.md" = @{
        "Target" = "Modelfile"
        "Section" = "SYSTEM"
        "Type" = "File"
    }
    "SP-002-clinerules-global.md" = @{
        "Target" = ".clinerules"
        "Section" = "Full"
        "Type" = "File"
    }
    "SP-003-persona-product-owner.md" = @{
        "Target" = ".roomodes"
        "Section" = "customModes[0].roleDefinition"
        "Type" = "JSON"
    }
    "SP-004-persona-scrum-master.md" = @{
        "Target" = ".roomodes"
        "Section" = "customModes[1].roleDefinition"
        "Type" = "JSON"
    }
    "SP-005-persona-developer.md" = @{
        "Target" = ".roomodes"
        "Section" = "customModes[2].roleDefinition"
        "Type" = "JSON"
    }
    "SP-006-persona-qa-engineer.md" = @{
        "Target" = ".roomodes"
        "Section" = "customModes[3].roleDefinition"
        "Type" = "JSON"
    }
    "SP-007-gem-gemini-roo-agent.md" = @{
        "Target" = "Gemini Web UI"
        "Section" = "N/A"
        "Type" = "Manual"
    }
}

# Initialisation
if (-not (Test-Path $QA_DIR)) {
    New-Item -ItemType Directory -Path $QA_DIR | Out-Null
}

# Générer un rapport Markdown
function Generate-Report {
    $reportLines = @()
    $reportLines += "# Rapport de Cohérence des System Prompts`n"
    $reportLines += "**Date :** $((Get-Date).ToString('yyyy-MM-dd'))`n"
    $reportLines += "**Phase :** 12 — Vérification automatique de cohérence`n"
    $reportLines += "**Statut :** Généré automatiquement`n`n"
    $reportLines += "--`-n`n"
    $reportLines += "## Résultats de Vérification`n`n"
    $reportLines += "| SP Canonique | Artefact Déployé | Statut | Notes |`n"
    $reportLines += "| :--- | :--- | :--- | :--- |`n"

    $allSynced = $true

    foreach ($spFile in $SP_MAPPING.Keys) {
        $spPath = "$PROMPTS_DIR\$spFile"
        $targetInfo = $SP_MAPPING[$spFile]
        $targetPath = if ($targetInfo.Type -eq "File") { "$PROJECT_ROOT\$($targetInfo.Target)" } else { $targetInfo.Target }

        $status = "❌ DÉSYNCHRONISÉ"
        $notes = ""

        if ($targetInfo.Type -eq "File") {
            if (-not (Test-Path $spPath)) {
                $status = "❌ FICHIER MANQUANT"
                $notes = "SP canonique introuvable"
            }
            elseif (-not (Test-Path $targetPath)) {
                $status = "❌ CIBLE MANQUANTE"
                $notes = "Artefact déployé introuvable"
            }
            else {
                # Extraire le contenu pertinent du SP
                $spContent = Get-Content -Path $spPath -Raw
n                # Extraire le contenu pertinent de la cible
                $targetContent = ""
                if ($targetInfo.Section -eq "Full") {
                    $targetContent = Get-Content -Path $targetPath -Raw
                }
                elseif ($targetInfo.Section -eq "SYSTEM") {
                    $targetContent = (Get-Content -Path $targetPath -Raw) -split "SYSTEM `"""" | Select-Object -Last 1
                    $targetContent = $targetContent -split "`"""" | Select-Object -First 1
                }
                elseif ($targetInfo.Type -eq "JSON" -and $targetInfo.Section -match "customModes\[(\d+)\]\.roleDefinition") {
                    $roomodes = Get-Content -Path $targetPath -Raw | ConvertFrom-Json
                    $index = [int]$matches[1]
                    $targetContent = $roomodes.customModes[$index].roleDefinition
                }

                # Comparaison
                if ($spContent -match 'SYSTEM """(.*)"""') {
                    $spContent = $matches[1].Trim()
                }

                if ($spContent -eq $targetContent) {
                    $status = "✅ SYNCHRONISÉ"
                }
                else {
                    $status = "❌ DÉSYNCHRONISÉ"
                    $notes = "Contenu différent"
                    $allSynced = $false
                }
            }
        }
        else {
            $status = "⚠️ HORS GIT"
            $notes = "Vérification manuelle requise"
        }

        $reportLines += "| `$spFile` | `$($targetInfo.Target) $($targetInfo.Section)` | $status | $notes |`n"
    }

    $reportLines += "`n--`-n`n"
    $reportLines += "## Statut Global`n"
    $reportLines += "- **Cohérence :** " + ($allSynced ? "✅ TOUS SYNCHRONISÉS" : "❌ DÉSYNCHRONISATIONS DÉTECTÉES") + "`n"
    $reportLines += "- **Action requise :** " + ($allSynced ? "Aucune" : "Corriger les désynchronisations") + "`n"

    # Écrire le rapport
    $reportLines | Out-File -FilePath $REPORT_FILE -Encoding utf8
    return $allSynced
}

# Vérifier si le rapport existe déjà et est à jour
$reportExists = Test-Path $REPORT_FILE
$filesChanged = $false

if ($reportExists) {
    $lastReportDate = [datetime]::ParseExact((Get-Item $REPORT_FILE).Basename.Substring(12), 'yyyy-MM-dd', $null)
    $today = (Get-Date).Date

    # Vérifier si des fichiers ont changé depuis le dernier rapport
    $spFiles = Get-ChildItem -Path $PROMPTS_DIR -Filter "SP-*.md"
    foreach ($file in $spFiles) {
        if ($file.LastWriteTime -gt $lastReportDate) {
            $filesChanged = $true
            break
        }
    }

    if (-not $Force -and $today -eq $lastReportDate -and -not $filesChanged) {
        Write-Host "Rapport déjà à jour : $REPORT_FILE"
        exit 0
    }
}

# Générer le rapport
$isSynced = Generate-Report

# Retourner le code de sortie approprié
if ($isSynced) {
    Write-Host "✅ Tous les prompts sont synchronisés"
    exit 0
}
else {
    Write-Host "❌ Désynchronisations détectées - voir $REPORT_FILE"
    exit 1
}