import re
import pandas as pd
import sys

def process_data(raw_file, output_file="result.csv"):
    # Compile regex
    r_segmen1 = re.compile(r"[a-zA-Z]+-[a-zA-Z]+(\s?[a-zA-Z0-9])+")
    r_segmen2 = re.compile(r"[0-9]{51}")
    r_segmen3 = re.compile(r"[0-9]+[a-zA-Z/]{3}[0-9]+")
    r_segmen4 = re.compile(r"\s+[0-9]{2}[a-zA-Z0-9]{10}\s")
    r_segmen5 = re.compile(r"[0-9]{3}-[0-9]{10}")
    r_segmen6 = re.compile(r"\s{9}[a-zA-Z]+(\s[a-zA-Z]+)*")

    results = []
    i = 1
    with open(raw_file, encoding = 'utf-8') as f:
      for line in f:
        line = line.strip() # Membersihkan spasi di awal dan di akhir kalimat
        data = []

        # Memproses setiap baris
        if (len(line) > 0):
          print(f"Memproses baris ke-{i}: {line}")
          data.append(r_segmen1.search(line)[0].strip())
          data.append(r_segmen2.search(line)[0].strip())
          data.append(r_segmen3.search(line)[0].strip())
          data.append(r_segmen4.search(line)[0].strip())
          data.append(r_segmen5.search(line)[0].strip())
          data.append(r_segmen6.search(line)[0].strip())
          print(data)
          
          results.append(data)
          i = i + 1

    # Simpan ke CSV
    cols = ["segmen1", "segmen2", "segmen3", "segmen4", "segmen5", "segmen6"]
    df = pd.DataFrame(results, columns = cols)
    df.to_csv(output_file, header=True, index=False)

if __name__ == "__main__":

    # Penggunaan:
    #   python data-cleansing.py <nama file input> <nama file output>
    # Contoh:
    #   python data-cleansing.py "DATA-RAW.txt" "output.csv"
    
    raw_file = sys.argv[1]
    output_file = sys.argv[2]
    process_data(raw_file, output_file)
    print("Proses selesai.")
