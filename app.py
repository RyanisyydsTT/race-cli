import click
import shlex

@click.command()
@click.option('--help')
def help():
    raise NotImplementedError

@click.command()
@click.argument("cmd1", required=True)
@click.argument("cmd2", required=True)
def race(cmd1, cmd2):
    cmd1_elapsed, cmd1_exitcode = benchmark(cmd1)
    cmd2_elapsed, cmd2_exitcode = benchmark(cmd2)
    if cmd1_exitcode != 0 and cmd2_exitcode != 0:
        result = f"""Both command failed benchmarking
        Command 1 Exit Code: {cmd1_exitcode}
        Command 2 Exit Code: {cmd2_exitcode}
        """
    elif cmd1_exitcode != 0:
        result = f"Command 1 failed benchmarking, exit code {cmd1_exitcode}"
    elif cmd2_exitcode != 0:
        result = f"Command 2 failed benchmarking, exit code {cmd2_exitcode}"
    else:
        if cmd1_elapsed > cmd2_elapsed:
            pass
        elif cmd1_elapsed < cmd2_elapsed:
            pass
        else:
            pass

    click.echo(f"""
    BENCHMARK RESULT

    {result}
    """)

def benchmark(cmd):
    click.echo(f"Benchmarking {cmd}...")
    counter = time.perf_counter()

    process = subprocess.run(shlex.split(cmd), stdout=subproess=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    process_took = time.perf_counter() - counter
    exit_code = process.returncode
    
    #click.echo(f"Command 1 took {process_took:.4f}s, exit code {exit_code}")
    return process_took, exit_code



def greet():
    click.echo("""
Race CLI 1.0.0
A powerful tool to measure executive efficiency! Made w/ ♥  by Ryan Tseng.

Type --help for more information.""")

if __name__ == '__main__':
    greet()

def execute
