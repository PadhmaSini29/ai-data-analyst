import pandas as pd
import io
import contextlib

def execute_code(code: str, df: pd.DataFrame):
    local_env = {"df": df.copy(), "pd": pd}
    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, local_env)
        output = stdout.getvalue()
        result = local_env.get("result", output)
        return result, None
    except Exception as e:
        return None, str(e)
