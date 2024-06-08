from use import use
import argparse
import pyfiglet


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_section(self, heading):
        heading = f"{Colors.CYAN}{heading}{Colors.ENDC}"
        super().start_section(heading)

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = f"{Colors.GREEN}Usage: {Colors.ENDC}"
        return super()._format_usage(usage, actions, groups, prefix)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return f"{Colors.YELLOW}{action.dest}{Colors.ENDC}"
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(f'{Colors.OKBLUE}{option_string}{Colors.ENDC} {args_string}')
            return ', '.join(parts)

class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def print_help(self, file=None):
        self._print_message(self.format_help(), file)

parser = CustomArgumentParser(
    description=f"{Colors.YELLOW}LinkedIn Scraper{Colors.ENDC}",
    formatter_class=CustomHelpFormatter
)


def display_title():
    title = pyfiglet.figlet_format("LinkedIn Scraper", font="ogre")
    print(f"{Colors.YELLOW}{title}{Colors.ENDC}")

display_title()


# First, parse the arguments to check the --links flag
initial_parser = argparse.ArgumentParser(description="LinkedIn Scraper", add_help=False)
initial_parser.add_argument('--links', type=bool, default=False, help=f"{Colors.GREEN}Use links file{Colors.ENDC}")
initial_args, _ = initial_parser.parse_known_args()

# Set up the main parser with conditional requirements
parser = argparse.ArgumentParser(description="LinkedIn Scraper")
parser.add_argument('-o', '--occupation', type=str, required=not initial_args.links, help=f"{Colors.GREEN}Enter the occupation(s){Colors.ENDC}")
parser.add_argument('-loc', '--location', type=str, required=not initial_args.links, help=f"{Colors.GREEN}Enter the location{Colors.ENDC}")
parser.add_argument('-l', '--limit', type=int, required=False, default=1, help=f"{Colors.GREEN}Enter the number of page searches{Colors.ENDC}")
parser.add_argument('--cc', 'create_cookies', type=bool, default=False, help=f"{Colors.GREEN}Create cookies{Colors.ENDC}")
parser.add_argument('--links', type=bool, default=1, help=f"{Colors.GREEN}Use links file{Colors.ENDC}")
parser.add_argument('--vpn', type=str, help=f"{Colors.GREEN}Enter the location of VPN{Colors.ENDC}")

args = parser.parse_args()

print(f"{Colors.GREEN}Occupations: {', '.join(args.occ)}{Colors.ENDC}")
print(f"{Colors.GREEN}Location: {args.loc}{Colors.ENDC}")
print(f"{Colors.GREEN}Page Search Limit: {args.limit}{Colors.ENDC}")
print(f"{Colors.GREEN}Create Cookies: {args.cc}{Colors.ENDC}")
print(f"{Colors.GREEN}Use Links File: {args.links}{Colors.ENDC}")


if args.cc:
    print(f"{Colors.OKCYAN}Creating cookies...{Colors.ENDC}")
    uu = use(create_cookies=True)
    uu.run()

if not args.cc:
    # if args.vpn:
    #     uu = use(occupation=args.occupation, location=args.location, count=args.limit, vpn=args.vpn)
    #     uu.run()
    #     print(f"{Colors.GREEN}VPN Location: {args.vpn}{Colors.ENDC}")
    # else:
    uu = use(occupation=args.occupation, location=args.location, count=args.limit)
    uu.run()

if args.links:
    uu = use(use_links=True)
    uu.run()