<#
.SYNOPSIS
    Référence de déploiement — À exécuter depuis la racine de l'établi.

.DESCRIPTION
    Ce fichier est une COPIE DE RÉFÉRENCE déployée dans les projets applicatifs
    par l'établi agentic-agile-workbench.

    Il ne doit PAS être exécuté depuis ce dossier (scripts/).

    POUR METTRE À JOUR CE PROJET :
    ================================
    1. Aller dans le dépôt agentic-agile-workbench (l'établi)
    2. Exécuter le script canonique depuis sa racine :

       cd chemin\vers\agentic-agile-workbench
       .\deploy-to-project.ps1 -ProjectPath "chemin\vers\ce-projet" -Update

    Le script canonique se trouve à la RACINE de l'établi (pas dans template/scripts/).
    C'est lui qui contient la logique complète et la résolution correcte des chemins.

.NOTES
    Fichier déployé automatiquement par deploy-to-project.ps1 (racine de l'établi).
    Ne pas modifier ce fichier directement — modifier le script canonique dans l'établi.
#>

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Yellow
Write-Host "  ATTENTION : Ce script doit être exécuté depuis l'établi, pas depuis ici." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Ce fichier est une copie de référence déployée dans votre projet." -ForegroundColor White
Write-Host "  Pour mettre à jour ce projet, exécutez depuis la racine de l'établi :" -ForegroundColor White
Write-Host ""
Write-Host "    cd chemin\vers\agentic-agile-workbench" -ForegroundColor Cyan
Write-Host "    .\deploy-to-project.ps1 -ProjectPath `"$(Split-Path -Parent $PSScriptRoot)`" -Update" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Yellow
Write-Host ""
exit 1
