import os

base_dir = r"d:\Downloads\Project - Q 30 (Day)\quantum-platform-enterprise\backend\quantum_engine"

files = {
    # DTO updates (Capabilities & Extended Report)
    "dto/provider.py": """
from pydantic import BaseModel

class ProviderCapabilities(BaseModel):
    supports_runtime: bool
    supports_sampler: bool
    supports_estimator: bool
    supports_dynamic_circuits: bool
    supports_pulse: bool
    supports_noise: bool
    supports_real_hardware: bool
    supports_simulator: bool
""",
    # Update Execution Report with Phase 6 fields
    "dto/execution.py": """
from pydantic import BaseModel
from typing import Dict, Any, Optional
from dto.circuit import CircuitExecutionRequest, CircuitExecutionResponse

class ExecutionReport(BaseModel):
    execution_id: str
    compilation_time_ms: float
    execution_time_ms: float
    queue_time_ms: float = 0.0
    provider_name: str
    provider_version: Optional[str] = None
    backend_name: str
    backend_version: Optional[str] = None
    runtime_version: Optional[str] = None
    simulator_type: str
    optimization_level: int
    ibm_job_id: Optional[str] = None
    warnings: list[str] = []
    errors: list[str] = []
    statistics: Dict[str, Any] = {}
""",
    # Exceptions mapped to IBM
    "exceptions/ibm_exceptions.py": """
from exceptions.quantum_exceptions import (
    QuantumEngineError, ProviderAuthError, BackendOffline,
    HardwareQueueError, ExecutionTimeout
)
import logging

logger = logging.getLogger(__name__)

def map_ibm_exception(e: Exception) -> QuantumEngineError:
    err_str = str(e).lower()
    if "auth" in err_str or "unauthorized" in err_str:
        logger.error("Provider Authentication Error (Details masked)")
        return ProviderAuthError("Failed to authenticate with IBM Quantum.")
    if "offline" in err_str or "not found" in err_str:
        return BackendOffline("The requested IBM backend is offline or not found.")
    if "queue" in err_str or "capacity" in err_str:
        return HardwareQueueError("Hardware queue overflow or capacity reached.")
    if "timeout" in err_str:
        return ExecutionTimeout("IBM Runtime job timed out.")
    return QuantumEngineError(f"IBM Execution Error: {str(e)}")
""",
    # IBM Provider
    "providers/ibm_provider.py": """
from interfaces.provider import QuantumProvider, QuantumBackend
from adapters.qiskit_adapter import QiskitAdapter
from dto.circuit import CircuitExecutionRequest, CircuitExecutionResponse
from dto.provider import ProviderCapabilities
from exceptions.ibm_exceptions import map_ibm_exception
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile
import uuid
import time
import logging

logger = logging.getLogger(__name__)

class IBMRuntimeBackend(QuantumBackend):
    def __init__(self, service: QiskitRuntimeService, backend_name: str):
        self.backend_name = backend_name
        self.service = service
        try:
            self.backend = service.backend(backend_name)
        except Exception as e:
            raise map_ibm_exception(e)
            
    def execute(self, request: CircuitExecutionRequest) -> CircuitExecutionResponse:
        start_time = time.time()
        
        try:
            # Transpilation
            qc = QiskitAdapter.to_qiskit(request.definition)
            comp_start = time.time()
            compiled_circuit = transpile(qc, self.backend, optimization_level=request.metadata.optimization_level)
            compilation_time = (time.time() - comp_start) * 1000
            
            # Execution using Sampler primitive
            sampler = Sampler(backend=self.backend)
            job = sampler.run([compiled_circuit], shots=request.shots)
            
            logger.info("Submitted job to IBM Runtime", extra={"ibm_job_id": job.job_id()})
            
            result = job.result()
            
            # Parsing primitives V2 output
            pub_result = result[0]
            counts = pub_result.data.c.get_counts() if hasattr(pub_result.data, "c") else {}
            
            execution_time = (time.time() - start_time) * 1000
            
            return CircuitExecutionResponse(
                job_id=job.job_id(),
                status=job.status().name,
                counts=counts,
                execution_time_ms=execution_time
            )
        except Exception as e:
            raise map_ibm_exception(e)

class IBMProvider(QuantumProvider):
    def __init__(self, api_token: str):
        try:
            self.service = QiskitRuntimeService(channel="ibm_quantum", token=api_token)
        except Exception as e:
            raise map_ibm_exception(e)
            
    def get_backend(self, name: str) -> QuantumBackend:
        return IBMRuntimeBackend(self.service, name)
        
    def available_backends(self) -> list:
        backends = self.service.backends()
        return [b.name for b in backends]

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            supports_runtime=True,
            supports_sampler=True,
            supports_estimator=True,
            supports_dynamic_circuits=True,
            supports_pulse=True,
            supports_noise=True,
            supports_real_hardware=True,
            supports_simulator=True
        )
""",
    # Factory Update
    "providers/factory.py": """
from interfaces.provider import QuantumProvider
from exceptions.quantum_exceptions import ProviderUnavailable
from providers.aer_provider import AerProvider
from providers.ibm_provider import IBMProvider

class QuantumProviderFactory:
    @staticmethod
    def get_provider(provider_type: str, credentials: dict = None) -> QuantumProvider:
        if provider_type == "aer":
            return AerProvider()
        elif provider_type == "ibm":
            if not credentials or "api_token" not in credentials:
                raise ProviderUnavailable("IBM Provider requires an 'api_token' in credentials.")
            return IBMProvider(api_token=credentials["api_token"])
        else:
            raise ProviderUnavailable(f"Provider {provider_type} is not implemented.")
"""
}

import os
for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")

print("Phase 6 IBM Quantum Runtime Architecture Created.")
