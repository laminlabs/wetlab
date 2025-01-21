from __future__ import annotations

import re
from typing import TYPE_CHECKING, Literal, Optional, Tuple

import bionty as bt
import lamindb as ln
import pandas as pd
from lamin_utils import colors, logger

try:
    from cellxgene_lamin import CellxGeneFields
    from cellxgene_lamin import Curate as CellxGeneCurate
except ImportError:
    CellxGeneFields = "CellxGeneFields"

    class CellxGeneCurate:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "cellxgene_lamin is not installed. Please install it to use PertCurator."
            )


from .models import (
    Biologic,
    Compound,
    Donor,
    EnvironmentalPerturbation,
    GeneticPerturbation,
    PerturbationTarget,
)

if TYPE_CHECKING:
    import anndata as ad
    from lamindb.base.types import FieldAttr


class ValidationError(SystemExit):
    """Validation error."""

    pass


class PertValidatorUnavailable(SystemExit):
    """Curator for perturbation data when dependencies are unavailable."""

    pass


class ValueUnit:
    """Base class for handling value-unit combinations."""

    @staticmethod
    def parse_value_unit(value: str, is_dose: bool = True) -> tuple[str, str] | None:
        """Parse a string containing a value and unit into a tuple."""
        if not isinstance(value, str) or not value.strip():
            return None

        value = str(value).strip()
        match = re.match(r"^(\d*\.?\d{0,1})\s*([a-zA-ZμµΜ]+)$", value)

        if not match:
            raise ValueError(
                f"Invalid format: {value}. Expected format: number with max 1 decimal place + unit"
            )

        number, unit = match.groups()
        formatted_number = f"{float(number):.1f}"

        if is_dose:
            standardized_unit = DoseHandler.standardize_unit(unit)
            if not DoseHandler.validate_unit(standardized_unit):
                raise ValueError(
                    f"Invalid dose unit: {unit}. Must be convertible to one of: nM, μM, mM, M"
                )
        else:
            standardized_unit = TimeHandler.standardize_unit(unit)
            if not TimeHandler.validate_unit(standardized_unit):
                raise ValueError(
                    f"Invalid time unit: {unit}. Must be convertible to one of: h, m, s, d, y"
                )

        return formatted_number, standardized_unit


class DoseHandler:
    """Handler for dose-related operations."""

    VALID_UNITS = {"nM", "μM", "µM", "mM", "M"}
    UNIT_MAP = {
        "nm": "nM",
        "NM": "nM",
        "um": "μM",
        "UM": "μM",
        "μm": "μM",
        "μM": "μM",
        "µm": "μM",
        "µM": "μM",
        "mm": "mM",
        "MM": "mM",
        "m": "M",
        "M": "M",
    }

    @classmethod
    def validate_unit(cls, unit: str) -> bool:
        """Validate if the dose unit is acceptable."""
        return unit in cls.VALID_UNITS

    @classmethod
    def standardize_unit(cls, unit: str) -> str:
        """Standardize dose unit to standard formats."""
        return cls.UNIT_MAP.get(unit, unit)

    @classmethod
    def validate_values(cls, values: pd.Series) -> list:
        """Validate pert_dose values with strict case checking."""
        errors = []

        for idx, value in values.items():
            if pd.isna(value):
                continue

            if isinstance(value, (int, float)):
                errors.append(
                    f"Row {idx} - Missing unit for dose: {value}. Must include a unit (nM, μM, mM, M)"
                )
                continue

            try:
                ValueUnit.parse_value_unit(value, is_dose=True)
            except ValueError as e:
                errors.append(f"Row {idx} - {str(e)}")

        return errors


class TimeHandler:
    """Handler for time-related operations."""

    VALID_UNITS = {"h", "m", "s", "d", "y"}

    @classmethod
    def validate_unit(cls, unit: str) -> bool:
        """Validate if the time unit is acceptable."""
        return unit == unit.lower() and unit in cls.VALID_UNITS

    @classmethod
    def standardize_unit(cls, unit: str) -> str:
        """Standardize time unit to standard formats."""
        if unit.startswith("hr"):
            return "h"
        elif unit.startswith("min"):
            return "m"
        elif unit.startswith("sec"):
            return "s"
        return unit[0].lower()

    @classmethod
    def validate_values(cls, values: pd.Series) -> list:
        """Validate pert_time values."""
        errors = []

        for idx, value in values.items():
            if pd.isna(value):
                continue

            if isinstance(value, (int, float)):
                errors.append(
                    f"Row {idx} - Missing unit for time: {value}. Must include a unit (h, m, s, d, y)"
                )
                continue

            try:
                ValueUnit.parse_value_unit(value, is_dose=False)
            except ValueError as e:
                errors.append(f"Row {idx} - {str(e)}")

        return errors


class PertCurator(CellxGeneCurate):
    """Curator flow for Perturbation data."""

    PERT_COLUMNS = {"compound", "genetic", "biologic", "physical"}

    def __init__(
        self,
        adata: ad.AnnData,
        var_index: FieldAttr = bt.Gene.ensembl_gene_id,
        organism: Literal["human", "mouse"] = "human",
        pert_dose: bool = True,
        pert_time: bool = True,
        *,
        verbosity: str = "hint",
        cxg_schema_version: Literal["5.0.0", "5.1.0"] = "5.1.0",
        using_key: str | None = None,
    ):
        """Initialize the curator with configuration and validation settings."""
        if isinstance(CellxGeneFields, str):
            CellxGeneCurate()

        self._pert_time = pert_time
        self._pert_dose = pert_dose

        self._validate_initial_data(adata)
        self._setup_configuration(adata)

        self._setup_sources(adata, using_key)
        self._setup_compound_source()

        super().__init__(
            adata=adata,
            var_index=var_index,
            categoricals=self.PT_CATEGORICALS,
            using_key=using_key,
            defaults=self.PT_DEFAULT_VALUES,
            verbosity=verbosity,
            organism=organism,
            extra_sources=self.PT_SOURCES,
            schema_version=cxg_schema_version,
        )

    def _setup_configuration(self, adata: ad.AnnData):
        """Set up default configuration values."""
        self.PT_DEFAULT_VALUES = CellxGeneFields.OBS_FIELD_DEFAULTS | {
            "cell_line": "unknown",
            "pert_target": "unknown",
        }

        self.PT_CATEGORICALS = CellxGeneFields.OBS_FIELDS | {
            k: v
            for k, v in {
                "cell_line": bt.CellLine.name,
                "pert_target": PerturbationTarget.name,
                "pert_genetic": GeneticPerturbation.name,
                "pert_compound": Compound.name,
                "pert_biologic": Biologic.name,
                "pert_physical": EnvironmentalPerturbation.name,
            }.items()
            if k in adata.obs.columns
        }
        # if "donor_id" in self.PT_CATEGORICALS:
        #     self.PT_CATEGORICALS["donor_id"] = Donor.name

    def _setup_sources(self, adata: ad.AnnData, using_key: str):
        """Set up data sources."""
        self.PT_SOURCES = {}
        # if "cell_line" in adata.obs.columns:
        #     self.PT_SOURCES["cell_line"] = (
        #         bt.Source.using(using_key).filter(name="depmap").first()
        #     )
        if "pert_compound" in adata.obs.columns:
            self.PT_SOURCES["pert_compound"] = (
                bt.Source.using(using_key)
                .filter(entity="wetlab.Compound", name="chebi")
                .first()
            )

    def _validate_initial_data(self, adata: ad.AnnData):
        """Validate the initial data structure."""
        self._validate_required_columns(adata)
        self._validate_perturbation_types(adata)

    def _validate_required_columns(self, adata: ad.AnnData):
        """Validate required columns are present."""
        if "pert_target" not in adata.obs.columns:
            if (
                "pert_name" not in adata.obs.columns
                or "pert_type" not in adata.obs.columns
            ):
                raise ValidationError(
                    "either 'pert_target' or both 'pert_name' and 'pert_type' must be present"
                )
        else:
            if "pert_name" not in adata.obs.columns:
                logger.warning(
                    "no 'pert' column found in adata.obs, will only curate 'pert_target'"
                )
            elif "pert_type" not in adata.obs.columns:
                raise ValidationError("both 'pert' and 'pert_type' must be present")

    def _validate_perturbation_types(self, adata: ad.AnnData):
        """Validate perturbation types."""
        if "pert_type" in adata.obs.columns:
            data_pert_types = set(adata.obs["pert_type"].unique())
            invalid_pert_types = data_pert_types - self.PERT_COLUMNS
            if invalid_pert_types:
                raise ValidationError(
                    f"invalid pert_type found: {invalid_pert_types}!\n"
                    f"    → allowed values: {self.PERT_COLUMNS}"
                )
            self._process_perturbation_types(adata, data_pert_types)

    def _process_perturbation_types(self, adata: ad.AnnData, pert_types: set):
        """Process and map perturbation types."""
        for pert_type in pert_types:
            col_name = "pert_" + pert_type
            adata.obs[col_name] = adata.obs["pert_name"].where(
                adata.obs["pert_type"] == pert_type, None
            )
            if adata.obs[col_name].dtype.name == "category":
                adata.obs[col_name].cat.remove_unused_categories()
            logger.important(f"mapped 'pert_name' to '{col_name}'")

    def _setup_compound_source(self):
        """Set up the compound source with muted logging."""
        with logger.mute():
            chebi_source = bt.Source.filter(
                entity="wetlab.Compound", name="chebi"
            ).first()
            if not chebi_source:
                Compound.add_source(
                    bt.Source.filter(entity="Drug", name="chebi").first()
                )

    def validate(self) -> bool:
        """Validate the AnnData object."""
        validated = super().validate()

        if self._pert_dose:
            validated &= self._validate_dose_column()
        if self._pert_time:
            validated &= self._validate_time_column()

        self._validated = validated

        # sort columns
        first_columns = [
            "pert_target",
            "pert_genetic",
            "pert_compound",
            "pert_biologic",
            "pert_physical",
            "pert_dose",
            "pert_time",
            "organism",
            "cell_line",
            "cell_type",
            "disease",
            "tissue_type",
            "tissue",
            "assay",
            "suspension_type",
            "donor_id",
            "sex",
            "self_reported_ethnicity",
            "development_stage",
            "pert_name",
            "pert_type",
        ]
        sorted_columns = [
            col for col in first_columns if col in self._adata.obs.columns
        ] + [col for col in self._adata.obs.columns if col not in first_columns]
        # must assign to self._df to ensure .standardize works correctly
        self._df = self._adata.obs[sorted_columns]
        self._adata.obs = self._df
        return validated

    def standardize(self, key: str) -> pd.DataFrame:
        """Standardize the AnnData object."""
        super().standardize(key)
        self._adata.obs = self._df

    def _validate_dose_column(self) -> bool:
        """Validate the dose column."""
        if not ln.Feature.filter(name="pert_dose").exists():
            ln.Feature(name="pert_dose", dtype="str").save()

        dose_errors = DoseHandler.validate_values(self._adata.obs["pert_dose"])
        if dose_errors:
            self._log_validation_errors("pert_dose", dose_errors)
            return False
        return True

    def _validate_time_column(self) -> bool:
        """Validate the time column."""
        if not ln.Feature.filter(name="pert_time").exists():
            ln.Feature(name="pert_time", dtype="str").save()

        time_errors = TimeHandler.validate_values(self._adata.obs["pert_time"])
        if time_errors:
            self._log_validation_errors("pert_time", time_errors)
            return False
        return True

    def _log_validation_errors(self, column: str, errors: list):
        """Log validation errors with formatting."""
        errors_print = "\n    ".join(errors)
        logger.warning(
            f"invalid {column} values found!\n    {errors_print}\n"
            f"    → run {colors.cyan('standardize_dose_time()')}"
        )

    def standardize_dose_time(self) -> pd.DataFrame:
        """Standardize dose and time values."""
        standardized_df = self._adata.obs.copy()

        if "pert_dose" in self._adata.obs.columns:
            standardized_df = self._standardize_column(
                standardized_df, "pert_dose", is_dose=True
            )

        if "pert_time" in self._adata.obs.columns:
            standardized_df = self._standardize_column(
                standardized_df, "pert_time", is_dose=False
            )

        self._adata.obs = standardized_df
        return standardized_df

    def _standardize_column(
        self, df: pd.DataFrame, column: str, is_dose: bool
    ) -> pd.DataFrame:
        """Standardize values in a specific column."""
        for idx, value in self._adata.obs[column].items():
            if pd.isna(value) or (
                isinstance(value, str) and (not value.strip() or value.lower() == "nan")
            ):
                df.at[idx, column] = None
                continue

            try:
                num, unit = ValueUnit.parse_value_unit(value, is_dose=is_dose)
                df.at[idx, column] = f"{num}{unit}"
            except ValueError:
                continue

        return df
