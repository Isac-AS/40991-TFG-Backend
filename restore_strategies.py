from src import app, db
from src.strategies.models import Strategy

def restore_strategies():
    strategy_name = "whisper"
    description = "Estrategia de conversión de voz a texto usando la herramienta 'whisper' de openai"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Voz a texto")
    db.session.add(strategy)
    strategy_name = "whisper_small"
    description = "Estrategia de transcripción que usa el modelo 'small' de whisper."
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Voz a texto")
    db.session.add(strategy)
    strategy_name = "pyspellchecker"
    description = "Estrategia empleada para corregir posibles errores ortográficos de la transcripción"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Intermedia")
    db.session.add(strategy)
    strategy_name = "sample_adt_a01"
    description = "Estrategia de ejemplo para crear una historia clínica electrónica"
    file_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-strategy.py'
    env_path = f'/opt/40991-TFG-Backend/src/strategies_implementations/{strategy_name}-strategy/{strategy_name}-venv/bin/python'
    strategy = Strategy(name=strategy_name, description=description, env_path=env_path, python_file_path=file_path, input_type="string", output_type="string",
                        created_by="admin", last_modified_by="admin", stage="Final")
    db.session.add(strategy)
    db.session.commit()