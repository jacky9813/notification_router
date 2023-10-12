import argparse
import sys

import parver


CLASSIFIERS = [
    "Framework :: Flask",
    "Intended Audience :: Information Technology",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Communications",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    "Topic :: System :: Monitoring"
]


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", "-o", type=argparse.FileType("w"), default=sys.stdout)
    parser.add_argument("version")

    args = parser.parse_args()

    version = parver.Version.parse(args.version)
    if version.is_devrelease:
        CLASSIFIERS.append("Development Status :: 2 - Pre-Alpha")
    elif version.is_alpha:
        CLASSIFIERS.append("Development Status :: 3 - Alpha")
    elif version.is_beta or version.is_release_candidate:
        CLASSIFIERS.append("Development Status :: 4 - Beta")
    else:
        CLASSIFIERS.append("Development Status :: 5 - Production/Stable")

    
    for classifiers in sorted(CLASSIFIERS):
        print(classifiers, file=args.output)


if __name__ == "__main__":
    main()
