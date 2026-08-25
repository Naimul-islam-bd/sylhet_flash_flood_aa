# -----------------------------------------------------------------------------
# Sylhet AA Pipeline - Makefile
# -----------------------------------------------------------------------------
# Common commands. Run `make help` to see all targets.
#
# Windows users: install `make` via chocolatey (`choco install make`) or use
# WSL, or run the underlying Python commands directly (they are all shown).
# -----------------------------------------------------------------------------

PYTHON ?= python
CHIRPS ?= data/raw/sylhet_chirps_daily_1981_2024.csv
ERA5   ?= data/raw/sylhet_era5land_daily_1950_2024.csv
EVENTS ?= data/raw/events_catalogue.csv

.PHONY: help install install-dev test lint format \
        stage-a stage-a-era5 stage-b stage-d figures \
        clean clean-outputs

help:
	@echo "Sylhet AA Pipeline - available targets:"
	@echo ""
	@echo "  install         Install the package (production dependencies only)"
	@echo "  install-dev     Install with dev tools (pytest, ruff, black)"
	@echo "  install-all     Install everything (geo extras + dev tools)"
	@echo "  test            Run unit tests"
	@echo "  lint            Run ruff linter"
	@echo "  format          Format code with black"
	@echo ""
	@echo "  stage-a         Run Stage A trend analysis on CHIRPS"
	@echo "  stage-a-era5    Run Stage A trend analysis on ERA5-Land (long-term)"
	@echo "  stage-b         Run Stage B flood accuracy (needs S1 rasters)"
	@echo "  stage-d         Run Stage D trigger thresholds"
	@echo "  figures         Generate all publication-quality figures"
	@echo ""
	@echo "  clean           Remove Python cache and build artifacts"
	@echo "  clean-outputs   Also remove generated outputs (dangerous)"

install:
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

install-all:
	$(PYTHON) -m pip install -e ".[all]"

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m ruff check src/ tests/ scripts/

format:
	$(PYTHON) -m black src/ tests/ scripts/

stage-a:
	$(PYTHON) scripts/01_run_stage_a_trends.py --input $(CHIRPS) --outdir outputs/stage_a

stage-a-era5:
	$(PYTHON) scripts/01_run_stage_a_trends.py --input $(ERA5) --outdir outputs/stage_a_era5 --label era5

stage-b:
	@echo "Stage B requires per-event GeoTIFFs. Run per event:"
	@echo "  $(PYTHON) scripts/02_run_flood_accuracy.py \\"
	@echo "      --predicted data/raw/ev_2022_jun_flood_extent.tif \\"
	@echo "      --reference data/raw/ev_2022_jun_s2_reference_water.tif \\"
	@echo "      --event_id ev_2022_jun --outdir outputs/stage_b"

stage-d:
	$(PYTHON) scripts/03_run_stage_d_thresholds.py \
		--rain $(CHIRPS) --events $(EVENTS) --outdir outputs/stage_d

figures:
	$(PYTHON) scripts/04_generate_paper_figures.py --outdir outputs/figures

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-outputs:
	rm -rf outputs/stage_a/* outputs/stage_a_era5/* outputs/stage_b/* outputs/stage_d/* outputs/figures/*
	@echo "All generated outputs cleared."
