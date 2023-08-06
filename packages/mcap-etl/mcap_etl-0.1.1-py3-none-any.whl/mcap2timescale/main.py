import argparse
import job


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="Path to rosbag or mcap file")

    parser.add_argument("-g", "--host", default='localhost', help="Postgres host")
    parser.add_argument("-p", "--port", default='5432', help="Postgres port")
    parser.add_argument("-u", "--user", default='postgres', help="Postgres user")
    parser.add_argument("-w", "--password", default='password', help="Postgres password")
    parser.add_argument("-n", "--name", default='postgres', help="Postgres database name")

    args = parser.parse_args()

    job.run(args.file, args.host, args.port, args.user, args.password, args.name)
