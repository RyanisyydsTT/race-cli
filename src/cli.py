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

def main():
    race()


# Below this description is a bag of Kuai Kuai (乖乖), it's a Taiwanese snack with a special place
# in engineering culture. Engineers often place a green bag
# of Kuai Kuai next to servers, computers, and other equipment,
# hoping the machines will "behave" and keep running smoothly.
#
# Why green? Green means everything is working normally.
# And "Kuai Kuai" literally means "be good" or "behave."
#
# Please do not eat it. :>

""""
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMN00KKKKXXXNNNNNNNNNNNNNNNNNNNNNNNWWNWWWWWWWWWWWWWWWWWWWWWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWMWWWWNNNNNXXXXNMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMM0oooooodddxxkkkkkkkkkkkkkkkkkkkkkkkkkkkkkOOOOOOOOOOOOOOOO0000000000000KKKKK0000000000000000000OOOOOkkkxxdddooo0WMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMM0oooollooddddddxxxxxxxxxdxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxdddddoooollOWMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMKxddooooodddxxxxxxxxkxxxxxkxxxkkxxxkkxxkxxxxkxxxxkkxxkkxxkkkkxxxkxxkkkkkkkkkkkkkkkkkkkkkkxxxxxxxxxxxdddddodollOWMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMNkddxddxxkkkkkkkkkOOOOOkkkOkkOOOkkOOOkkOOkkkOOkkkOOOkOOOkOOOOOkkOOOOOOOOOOOOOOOOOOOOOOOOkkkkkkkkkkkkkkxxxxdoodKWMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMXxoddxxkkkOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOkkkkkkkkkkkkkkkkkOOOOOkkkOOOOkkOOOkkxxddolldKWMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMNOddxxxxkkkkxdolclllodkOOOOOOOOOOOOkOOOOOOkkOkxkOOOOOOOOOOOOOOkkkxxxxkkkkkOOOkOOOkOOkOkkOOOkxddddddxdddookNMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMWXOxxkkkkdc;,,,,,,,,,:oxxkOkxl:::ldxc;clodxo,,cccclxkkkOOOOOOOkkxxxxxkkkOOO0K0OkOKOxOOkkkkkxc,:lc;lxxdoOWMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXkdkkOxlcooo:,,:lool:cxOd,'';::c,.'c:,,::.'c:;,;:okkkkkOOOOOkkkxxkkkkOOOO0K0OkOK0OkkOkkxkd'.::;,:odlkNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoldkOddO00Oxc;dO0Oko;oO:.,,;:cl;..;''.;lc,.;cc::dkOOkkkOOOOOkkkkOOOOOOOOOOOkkOK00OkOOkkkx:;clllldolOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKolokOxk00kkOo:xOkkkx;lOl.;l,;olc'.:ol',ox;.cl:ldxkkOkkkkOOOOOOOOOOOOOkkOO0OkkkkOOkOOOOOOxdodxxxdolckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKocldOOkxxkoc::::oo:::dOOo,:ccll:;cldo:cdxocllldkkkkkOkkkOOOOOOOOOOkdc::coxOOOOkOOkOOOkkOo;cdxxocclcxWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0olodk00kxxolc::cl:,;okOOOkxxxxxxkOOOOkkkkkkkxxxxxkkkOkkkOOOkkxxddl;:c;,,,;:clllllokxdkkOdcdxdxdlclcxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lclox0K0Oxol:;;;:clxOOOOOOOkkddolccccccclloxkkkkOOkkkkkxoc:;,''....''....,,. .'::;,'ckkOd:ldddocclcdNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lcloxOKXXKOxoooodxkkOOkdlc::cllloooddooollc:okkkkkkkdc;,.................',..ckOOOo':kOko,;cooc;:lcxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lclodOKXXKK0OkkkkkOxo:::ldxk0Kkk0kd0Od00dkKddkkOOko;.....................',..o0Ok0x.'kOkc,:oxxl:clcxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0l:codOKXXXK0OOkkxl:;cdO0kkxcldllxxokOdOOok0xkOOOd;.......................',. .:ddc. .dOkxxkkkkkdlccxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0c:codOK000xxkdl:;:d00xkd;;dxxkOkkxxxxxxxkkkddOOo'........................',. ,oxxd; .dOkkkkkOOkxlccxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lclodkOxdolccclokOOOxod0Odddoc:;;;::;'..'::;lxl...........................,..dOkk0k''xOkkkkkOOOxlccxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lclodOKKK00OkkOd:lxOOOkdl:;:coddxdl;.....:xkxc............................,. ,odxo; 'xOkkkkOOOOxlccxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKlclodkXWWKOko;cxddOkdc;:loxkkOkkl'........':;...,;,.....:oddxxdol:,.......'. .:ddc. 'xOkkkkOOOkxlccxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoclodkKXNKkO0kkOOdc;:ldkkOOkkkkkl.............,xKK0l..'lxclONWWWNkodo:...'c,.o0kO0x.'xOkkkkOOOkxllcxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXoclodkKK0Okkdol:;:ldkOOOkxxxddddd;............lXOxKx.:OKx:kNWNNWXd;;kXk;..::'ckOOOl.'xOkkkO00OOxllcxNMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXdclodkKK0kdlccloxkkkxddxkOO00Od:;c'...........lKKkOko0WNl'dNNNNKl:kKXNKc..,c,.'::,. 'dOkkO0000OxolckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXdclodk000OOOkkkkdooddxk0XWMMXxc;cxd'      ....'oO0XNKdlkK0XXKKNO;c0WNNo.'lxOko'......;xOO00KOdddollOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXdclodk00OOOkkxlloOOxddodkKNNXKklcdOd'  'cc'.   ,ONNNx. .l0XXXXNN0xkKNXdlOX00K0l'.,;...'coxxxolcclll0MMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNxclodk000OOko:l0WWKkkkXNWWNXXWWXo;oOx;,kWXc':;.;KWNNl  .dX0k0Xx:'.oKXNNNNKxONNNx;xXx,...':clllc,;llOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNxccoox000Oxl;dNMMWKkkkkxxdOKXWMWKc:xOxxXWOo0Xd.'ONNXo..'ldccOKo. ;0NNNNXX0OKXXW0cxXO:...,:llllc'.:lOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNxclooxO0Oko;lXWWWWWKOkdoooxKNWWWNd;dOxkNWXXXO:..lXNNOoddolclooc,:ONNNN0l,ckXXKxc;dKO:...,:llllc'.;lOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWxclodkOOOkl,dKxook0kxdkxoolkKOdkKocOK0KNNNWNXx' .c0NXOxxkkOOOkkkKNNNKko::cONNNc.,dKl....,:cllllccllkWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWkccldxkkkko;okccdddl:clc;,;o0OldxcoOO0KNNNNNOlc:,';d0KK0OOkkOOKXNNKOxdoooloKN0;..,;.....,:ldxkOxolckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWOccloxkkxkxl:ldxOkOkxxkOkdd0X0xoldOOOkkOOOOxllooolcckOOOOOO0000Okkxoddoooolol' ..    ..:oxOK00OxllckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWOllodxkkkkxxdloOXWMNK00OOXWWXkddkOOOOOkkkdlcccccccoOXkoxkdk00OOdodddoolc:;'..  ...';clxO00000OkdlcckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMM0llodxkkkkkkkkdodxOkxxxolxOkxxkkkkkOkkxkkkkxdooolcdOOdlllo0KK0kdddol:,'....',;..'ckkkkkOO00000kdllckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMM0lloxOOOOOOOOOOOOkxxxxxxxxkOOOkkkkkkkkkkkkkkkkkkko:llllollxOOkkxdoloddxxkkO000o:cx0000KKXXXXXXOolcckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMOlloxKXNNNNNNNNNNXXXXXNXXXXXXXXXXXXXXXXXXXXXXXXXXK0KKKKKKKXXXXXKKKKXNNNNNNNNNNNNNNWWWWWWWWWWWNOollckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWOllodONWWXKKXNNXKKXNNXKKXNWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMMMMMMMMMMMMMMMWKxlllckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWkclookXWXkkOOKKkkOOKKkOOOKMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWN0oclllkWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWkllolxKNN0OO0XN0OO0NN0O0KNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNklclllkWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMWxccllo0NWWWWMMMWWWMMMMWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXd:colckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNxcclllONWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNNNXXKKNWWNXXXXXKKXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKo:colckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMNxccoolkNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNkoolcllokX0olllcclldKWMMMMMMMMMMMMMMMMMMMMMMMMMMMMW0c;lolckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNxcloolkXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKdcccc:cldOxlc;c:ccclOWMMMMMMMMMMMMMMMMMMMMMMMMMMMMWk:;lolckWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNdcllolxXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXkl:clccookOo:,clcclokWMMMMMMMMMMMMMMMMMMMMMMMMMMMWNx;;lollOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMNdclloldXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXOxdoloxxxO0kdodloxxdOWMMMMMMMMMMMMMMMMMMMMMMMMMMMWNx,:oollOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMXdclodldKWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWXKXWWWWWWWWNKXWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWXd,coollOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoclododKWWWXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXNWWXo,colllOWMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKlclloldKWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXl'lolccOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0l:cloldKWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXl,lollcOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lcllooxKWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXl,odollOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lcloddkXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXl;odollOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lcloddkXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXo;odollOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMOccloddOXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWXd:odolcOMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMOccloddOXNMWXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXNWWNx:odoll0MMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMOlcloddOXWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWNkcodoloKMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMOlclodx0NWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMW0lldoldKMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0lloodx0NWMMMMMMMMMMMMMMMMMMMN0KNNNX0KNXO0NNNX0KNXOO0O0XKOkKKkOKKOK0O0K0XWMMMMMMNKKKNWWXKKXWWXdldoldXMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMM0oloodxKNWMMMMMMMMMMMMMMMMMMMN00XNNX00NXO0XNNX00NKkO00KXKOk00kOKKO00k0K0KWMMMMMW0kOOOX0kOOOXWNOooolxNMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoloodkKNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWX000KWX0OOKNWWXxdolOWMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoloodOXNWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWNNWNNNXXXXKK0kdoo0MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKoclodkOOkkkkkkkkkkkkkkOOOOO000000KKKKKKKKKKKKKKK00000000000OOOOOOOOkkkkkkxxxxxxxddddooooooooooooloKMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKocloddxxollllllllllloooooodddxxxxxxxxxxxxxxxxxddddooddoollllccc::::::;;;;;;;::::::ccccclllllooodooONMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMKocloooddddddxxxxxxkkkxxkxxkxxxxxxkkkkkkkkkkkkkOkkk0KKKKK0OkkOkxxkkkxxddddxxddxxxdxxxxdddxddxddddoold0WMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMNOocccloodddxxxxxddxddddddddddddddddxxooxkxxkkxdxkxxx0K00000kxkkxoodxxxdddddxxxxxxxxxxxxxxxdddddddddoollxXWMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMWKoc::ccloooooooooooooollllllllllllllllooooooddddooooooddddddooooooooooooollloooooddddddddddooolllloooolllcl0WMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMW0l::cclllllolllllllllccclccccccccccccccccccccccccccccccccccc::::::::c::cccccccccclllllllllllcccccccccccllcccdXMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMWx:::cccllloololoooooooooddddddddoddddddddddoddddddooodooooodoooooooooooooooodddddddddoooooodoolloooooolllllcoXMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMWk::cccclooooollooddoddoddddddddddddddxxxdddddddddddddddddddddddddddddddddddddxxxdxxxxddddddddooodddddooooolldXMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMWOllooddxxxkkxxkkOkOOOOOOOOOOkkkkkxxkkkkkkkkkkkkOOOOOOOOOOOOOOkkkkkkkkkkkkkkkkkkxxxxxxxxxxxxxxdddddddddddooolxNMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMWNNNNNNWWWWWWWWWWWWWMWWWWWWWWWWWWWWWWWWWWWWWWWWWWWMMMMMMMMWWWWWWWWWWWWWWWWWWWNNNNNNNNNNNNNNNNNXXXXXXXXXKKK00KWMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
"""
