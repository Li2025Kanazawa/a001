import serial
import csv
import time
import threading  # スレッドを使用して送受信を並列化

# シリアルポートの設定
SERIAL_PORT = 'COM3'
Hzz = 115200
CSV_FILE = 'dataz_0.csv'

def receive_data(ser, csv_writer, file):
    print("Receiving data...")
    while True:
        try:
            # シリアルポートからデータを読み取る
            line = ser.readline().decode('utf-8').strip()  # データを受信してデコード
            if line:
                print(f"Received: {line}")

                # データを分割してリストに変換
                data = line.split(",")  # カンマ区切りで分割

                # CSVにデータを保存
                csv_writer.writerow(data)
                file.flush()  # バッファをディスクに書き込む

        except KeyboardInterrupt:
            print("\nTerminating receive thread...")
            break
        except Exception as e:
            print(f"Receive error: {e}")

def send_data(ser):
    print("Sending data...")
    while True:
        try:
            # ユーザーからデータを入力
            user_input = input("Enter data to send (type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting send thread...")
                break

            # シリアルポートに送信
            ser.write((user_input + "\n").encode('utf-8'))
            print(f"Sent: {user_input}")

        except KeyboardInterrupt:
            print("\nTerminating send thread...")
            break
        except Exception as e:
            print(f"Send error: {e}")

def main():
    # シリアルポートを開く
    try:
        ser = serial.Serial(SERIAL_PORT, Hzz, timeout=1)
        print(f"Connected to {SERIAL_PORT}")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    # CSVファイルの準備
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["送信回数", "圧力設定電圧(V)", "流量設定電圧(V)", "Valve位置", "目標速度", "速度", "速度（平滑化）",
                             "変位", "目標位置（増減）", "残り距離", "GP", "GP入力", "GI", "GI入力", "GD", "GD入力",
                             "PID入力", "FF入力", "E駆動count", "E従動速度", "E従動速度平滑化", "E従動count"])  # ヘッダー行

        try:
            # スレッドを作成して受信と送信を並列化
            receive_thread = threading.Thread(target=receive_data, args=(ser, csv_writer, file), daemon=True)
            receive_thread.start()

            send_thread = threading.Thread(target=send_data, args=(ser,), daemon=True)
            send_thread.start()

            # スレッドが終了するまで待機
            receive_thread.join()
            send_thread.join()

        except KeyboardInterrupt:
            print("\nTerminating program...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    main()
