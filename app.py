import click
import shlex
import time
import subprocess
import statistics

@click.command()
@click.option(
    "--runs",
    "-r",
    default=1,
    type=click.IntRange(min=1),
    help="Number of times to benchmark each command."
)
@click.argument("cmd1", required=True)
@click.argument("cmd2", required=True)
def race(cmd1, cmd2, runs):
    if runs == 1:
        cmd1_elapsed, cmd1_exitcode = benchmark(cmd1)
        cmd2_elapsed, cmd2_exitcode = benchmark(cmd2)
    else:
        cmd1_results = []
        cmd2_results = []

        cmd1_counter = 0
        cmd2_counter = 0
        while cmd1_counter <= runs:
            cmd1_elapsed, cmd1_exitcode = benchmark(cmd1)
            cmd1_results.append(cmd1_elapsed)
            cmd1_counter += 1
        while cmd2_counter <= runs:
            cmd2_elapsed, cmd2_exitcode = benchmark(cmd2)
            cmd2_results.append(cmd1_elapsed)
            cmd2_counter += 1

        cmd1_min = min(cmd1_results)
        cmd1_max = max(cmd1_results)
        cmd1_avg = statistics.mean(cmd1_results)
        cmd2_min = min(cmd2_results)
        cmd2_max = max(cmd2_results)
        cmd2_avg = statistics.mean(cmd2_results)
        
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
        if runs == 1:
            if cmd1_elapsed > cmd2_elapsed:
                result = f"""
                 Command 2 has won!
            
                Command 1 took {cmd1_elapsed:.4f}s
                Command 2 took {cmd2_elapsed:.4f}s
                """
            elif cmd1_elapsed < cmd2_elapsed:
                result = f"""
                🏆 Command 1 has won!

                Command 1 took {cmd1_elapsed:.4f}s
                Command 2 took {cmd2_elapsed:.4f}s
                """
            else:
                result = f"""
                🎊 It's a tie!

                Command 1 took {cmd1_elapsed:.4f}s
                Command 2 took {cmd2_elapsed:.4f}s
                """
        else:
            if cmd1_avg > cmd2_avg:
                result = f"""
                🏆 Command 2 has won!
            
                Format: min/max/avg:
                Command 1: {cmd1_min:.4f}s/{cmd1_max:.4f}s/{cmd1_avg:.4f}s
                Command 2: {cmd2_min:.4f}s/{cmd2_max:.4f}s/{cmd2_avg:.4f}s
                """
            elif cmd1_avg < cmd2_avg:
                result = f"""
                🏆 Command 1 has won!
            
                Format: min/max/avg:
                Command 1: {cmd1_min:.4f}s/{cmd1_max:.4f}s/{cmd1_avg:.4f}s
                Command 2: {cmd2_min:.4f}s/{cmd2_max:.4f}s/{cmd2_avg:.4f}s
                """
            else:
                result = f"""
                🎊 It's a tie!
                
                Format: min/max/avg:
                Command 1: {cmd1_min:.4f}s/{cmd1_max:.4f}s/{cmd1_avg:.4f}s
                Command 2: {cmd2_min:.4f}s/{cmd2_max:.4f}s/{cmd2_avg:.4f}s
                """

    
    click.echo(f"""
    BENCHMARK RESULT
    
    {result}
    """)

def benchmark(cmd):
    click.echo(f"Benchmarking {cmd}...")
    counter = time.perf_counter()

    process = subprocess.run(shlex.split(cmd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    process_took = time.perf_counter() - counter
    exit_code = process.returncode
    
    #click.echo(f"Command 1 took {process_took:.4f}s, exit code {exit_code}")
    return process_took, exit_code



if __name__ == '__main__':
    race()


