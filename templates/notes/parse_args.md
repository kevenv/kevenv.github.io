# Parse args in C

- POSIX
- TODO: `--long-option`

## Example
```C
#include <stddef.h> // NULL
#include <stdio.h> // printf
#include <stdlib.h> // atoi
#include <unistd.h> // getopt

int main(int argc, char* argv[])
{
	char* name = NULL;
	int r = 1;
	int opt;
	while ((opt = getopt(argc, argv, "n:r:vh")) != -1) {
		switch (opt) {
			case 'n':
				name = optarg;
				break;
			case 'r':
				r = atoi(optarg);
				break;
			case 'v':
				printf("parse_args v0.0\n");
				break;
			case 'h':
			default:
				print_usage(argv[0]);
				return 0;
		}
	}

	while (r--) {
		printf("hello %s\n", name ? name : "");
	}

	return 0;
}

void print_usage(char* argv0)
{
	printf("Usage: %s [-n <name>] [-r <repeat>] [-v] [-h]\n", argv0);
	printf("Options:\n");
	printf("  -n <name>: Greets <name> by name\n");
	printf("  -r <repeat>: Greets <repeat> times\n");
	printf("  -v: Print out the version\n");
	printf("  -h: Shows this help\n");
}
```

```
./app -h
./app -v
./app -n Keven -r 5
```

## References
- <https://pubs.opengroup.org/onlinepubs/9699919799/functions/getopt.html>
- <https://www.man7.org/linux/man-pages/man3/getopt.3.html>
- <https://en.wikipedia.org/wiki/Getopt>
- <https://www.youtube.com/watch?v=P7xNMby844k&list=WL&index=3>
