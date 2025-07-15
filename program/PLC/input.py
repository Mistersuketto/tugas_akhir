from fins import FinsClient


def main() -> None:
    client = FinsClient(host="192.168.1.28")
    client.connect()
    # response = client.memory_area_write("CIO10.0", b"\x00")
    # response = client.memory_area_write("CIO10.1", b"\x00")
    # response = client.memory_area_write("CIO10.2", b"\x00")
    # response = client.memory_area_write("CIO10.3", b"\x00")
    # response = client.memory_area_write("CIO10.4", b"\x00")
    # response = client.memory_area_write("CIO10.5", b"\x00")
    # response = client.memory_area_write("CIO10.6", b"\x00")
    # response = client.memory_area_write("CIO10.7", b"\x00")
    # memberi nilai 1 pada CIO10.0
    # response = client.memory_area_write("CIO10.0", b"\x01")
    # response = client.memory_area_write("CIO10.1", b"\x01")
    # response = client.memory_area_write("CIO10.2", b"\x01")
    # response = client.memory_area_write("CIO10.3", b"\x01")
    # response = client.memory_area_write("CIO10.4", b"\x01")
    # response = client.memory_area_write("CIO10.5", b"\x01")
    # response = client.memory_area_write("CIO10.6", b"\x01")
    # response = client.memory_area_write("CIO10.7", b"\x01")

    print("Data:", response.data)
    print("Code:", response.code)
    print("Status text:", response.status_text)

    client.close()


if __name__ == "__main__":
    main()