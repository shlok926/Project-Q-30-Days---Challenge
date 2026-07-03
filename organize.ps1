$days = 1..10
foreach ($i in $days) {
    $dayStr = "{0:D2}" -f $i
    $folderName = "Day_$dayStr"
    New-Item -ItemType Directory -Force -Path $folderName | Out-Null
    New-Item -ItemType Directory -Force -Path "$folderName\Solutions_and_Notes" | Out-Null
    
    # Move files matching the day
    # We use a regex match to be safer, or simple wildcard
    Get-ChildItem -Path . -File | Where-Object { $_.Name -match "Day\s*-\s*$dayStr" -or $_.Name -match "Day-$dayStr" } | Move-Item -Destination $folderName
}

# For Mini Project
New-Item -ItemType Directory -Force -Path "Mini_Project_1" | Out-Null
New-Item -ItemType Directory -Force -Path "Mini_Project_1\Solutions_and_Notes" | Out-Null
Get-ChildItem -Path . -File -Filter "*MINI PROJECT*.pdf" | Move-Item -Destination "Mini_Project_1"
Move-Item -Path "Quantum-Randomness-Lab" -Destination "Mini_Project_1" -ErrorAction SilentlyContinue

# Cleanup
Remove-Item -Path "extract.py" -ErrorAction SilentlyContinue
Remove-Item -Path "extract.txt" -ErrorAction SilentlyContinue
