import subprocess
import shlex

class TaskRunner:
    def __init__(self, context):
        self.context = context
        import queue
        self.job_queue = queue.Queue()

    def schedule_job(self, job):
        self.job_queue.put(job)

    def execute_background_task(self, command_str: str):
        """
        Executes a shell command safely without shell=True.
        """
        # FIXED: Use shlex.split and shell=False to prevent injection
        import shlex
        cmd_list = shlex.split(command_str)
        proc = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True
        )
        return proc.stdout, proc.stderr

async def run_async_task(self, command):
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.execute_background_task, command)