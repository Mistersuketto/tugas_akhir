from fins import FinsClient


def main() -> None:
    client = FinsClient(host="192.168.1.28")
    client.connect()
    response = client.memory_area_write("CIO10.0", b"\x01")
    # memberi nilai 1 pada CIO10.0

    print("Data:", response.data)
    print("Code:", response.code)
    print("Status text:", response.status_text)

    client.close()


if __name__ == "__main__":
    main()