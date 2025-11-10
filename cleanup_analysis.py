"""
Análisis de archivos para limpieza del proyecto
"""
import os
from pathlib import Path

print("=" * 70)
print("ANÁLISIS DE ARCHIVOS DEL PROYECTO")
print("=" * 70)

# Archivos de prueba/verificación (scripts temporales)
test_files = [
    "test_imports.py",
    "test_beta23.py",
    "verify_fix.py",
    "verify_beta23_path.py",
    "verify_stay_duration.py",
    "diagnose_beta23.py",
]

# Archivos de documentación (pueden consolidarse)
doc_files = [
    "DIAGRAMA_INTEGRACION.md",
    "RESUMEN_REORGANIZACION.md",
    "STAY_DURATION_IMPLEMENTADO.md",
    "RESUMEN.md",
    "REORGANIZACION_BACKEND.md",
    "REFACTOR_COMPLETE.md",
    "REFACTORING_REPORT.md",
    "README_GUI.md",
    "README_EFECTOS.md",
    "VERIFICACION_FINAL.md",
    "COMMIT_STRATEGY.md",
    "BUG_BETA23.md",
    "ANALISIS_FRONTEND_BACKEND.md",
]

print("\n📋 SCRIPTS DE PRUEBA/VERIFICACIÓN (candidatos a eliminar):")
print("-" * 70)
total_size = 0
for filename in test_files:
    filepath = Path(filename)
    if filepath.exists():
        size = filepath.stat().st_size
        total_size += size
        print(f"  ✓ {filename:40} ({size:,} bytes)")
    else:
        print(f"  ✗ {filename:40} (no existe)")

print(f"\n  Total: {len([f for f in test_files if Path(f).exists()])} archivos, {total_size:,} bytes")

print("\n📚 DOCUMENTACIÓN (revisar si consolidar):")
print("-" * 70)
doc_size = 0
for filename in doc_files:
    filepath = Path(filename)
    if filepath.exists():
        size = filepath.stat().st_size
        doc_size += size
        print(f"  ✓ {filename:40} ({size:,} bytes)")

print(f"\n  Total: {len([f for f in doc_files if Path(f).exists()])} archivos, {doc_size:,} bytes")

print("\n" + "=" * 70)
print("RECOMENDACIONES:")
print("=" * 70)

print("\n1. SCRIPTS DE PRUEBA:")
print("   Estos archivos fueron creados para debugging y ya no son necesarios.")
print("   Se pueden eliminar de forma segura.\n")

print("2. DOCUMENTACIÓN:")
print("   Hay múltiples archivos MD que documentan el mismo proceso.")
print("   Sugerencia: Consolidar en 2-3 archivos principales:")
print("   - README.md (documentación principal)")
print("   - REFACTORING.md (cambios de refactorización)")
print("   - BUGS_FIXED.md (bugs corregidos)")

print("\n¿Quieres que elimine los scripts de prueba? (S/N)")
