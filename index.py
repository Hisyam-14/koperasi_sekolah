#head
import csv
import pwinput
from prettytable import PrettyTable
from datetime import datetime

#function untuk menambahkan ID secara otomatis
def user_auto():
    with open('user.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        users = list(reader)
        if users:
            last_user = users[-1]
            return int(last_user['ID'])
        else:
            return 0

#function untuk ngecek barang pada tabel
def brg_ada(nama_brg, barang):
    for item in barang:
        if nama_brg.lower() == item['Nama Barang'].lower():
            return True
    return False
        
#function untuk update stok barang
def update_stok_brg(barang):
    with open('barang.csv', 'w', newline='') as csvfile:
        fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(barang)

#function untuk No barang secara otomatis
def brg_auto():
    with open('barang.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        items = list(reader)
        if items:
            last_items = items[-1]
            return int(last_items['Nomor'])
        else:
            return 0

#function untuk register
def register():
    role = 0
    saldo = 0
    user_id = user_auto() + 1
    print("=========================")
    print("        Register         ")
    nama = input("Nama : ")
    pw = pwinput.pwinput("Password : ", mask='*')
    print("=========================")
    with open('user.csv', 'a', newline='') as csvfile:
        fieldnames = ['ID','Username','Password','Role','Saldo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'ID' : user_id, 'Username' : nama, 'Password' : pw, 'Role' : role, 'Saldo' : saldo})
        print("Registrasi behasil!")

#function untuk login
def login():
    print("=========================")
    print("          Login          ")
    nama = input("Nama : ")
    pw = pwinput.pwinput("Password : ", mask='*')
    print("=========================")
    with open('user.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Username'] == nama and row['Password'] == pw:
                return int(row['ID']), row['Username'], int(row['Role']), float(row['Saldo'])
        else:
            print("Login gagal. Register Dulu!")
            return None, None, None, None 

#function untuk menampilkan tabel barang
def tampil_brg():
    try:
        with open('barang.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)

            if len(data) == 0:
                print("Data Tidak Ditemukan!")
                return
            
            header = data[0]
            tabel = PrettyTable(header)

            for row in data[1:]:
                tabel.add_row(row)
            tabel.padding_width = 5
            
            print(tabel)
    except:
        print("=========================")
        print("Data Tidak Ditemukan!")
        print("=========================")

#function untuk menambahkan barang
def input_brg():
    while True:
        tampil_brg()
        no_brg = brg_auto() + 1
        nama_brg = input("Masukkan Nama Barang : ")

        with open('barang.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            barang = list(reader)

        if brg_ada(nama_brg, barang):
            print("=========================")
            print("Nama barang sudah ada. Coba lagi dengan nama barang lain.")
            print("=========================")
            continue
        
        try:
            harga_brg = float(input("Masukkan Harga Barang : "))
            stok_brg = int(input("Masukkan Stok Barang : "))
            if harga_brg and stok_brg > 0:
                with open('barang.csv', 'a', newline='') as csvfile:
                    fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writerow({'Nomor' : no_brg, 'Nama Barang' : nama_brg, 'Harga' : harga_brg, 'Stok' : stok_brg})
                    print("Data Berhasil Ditambah!")
                    break
            else:
                print("=========================")
                print("Input Harus Lebih Dari 0!")
                print("=========================")
        except:
            print("=========================")
            print("Harga & Stok Harus Angka!")
            print("=========================")

#function untuk mengupdate barang
def update_brg():
    try:
        tampil_brg()
        no_brg = int(input("Masukkan nomor barang yang ingin diupdate : "))
        with open('barang.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            barang = list(reader)

        for item in barang:
            if no_brg == int(item['Nomor']):
                nama_brg = input("Masukkan nama barang : ")

                if brg_ada(nama_brg, barang):
                    print("=========================")
                    print("Nama barang sudah ada. Coba lagi dengan nama barang lain.")
                    print("=========================")
                    break
                try:
                    harga_brg = float(input("Masukkan harga : "))
                    stok_brg = int(input("Masukkan stok barang : "))
                    if harga_brg and stok_brg > 0:
                        item.update({'Nama Barang' : nama_brg, 'Harga' : harga_brg, 'Stok' : stok_brg})
                        print("Data Berhasil Diupdate!")
                        break
                    else:
                        print("=========================")
                        print("Input Harus Lebih Dari 0!")
                        print("=========================")
                except:
                    print("=========================")
                    print("Harga & Stock Harus Angka!")
                    print("=========================")
        else:
            print("=========================")
            print("Barang Tidak Ditemukan!")
            print("=========================")
                    
        with open('barang.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(barang)

    except:
        print("=========================")
        print("Harus Angka!")
        print("=========================")

#function untuk hapus barang
def delete_brg():
    try:
        tampil_brg()
        no_brg = int(input("Masukkan nomor barang yang mau dihapus : "))

        with open('barang.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            brg = list(reader)

        updated_brg = [item for item in brg if int(item['Nomor']) != no_brg]

        if len(brg) != len(updated_brg):
            print("Berhail dihapus!")
        else:
            print("=========================")
            print("Barang Tidak Ditemukan!")
            print("=========================")

        for i, item in enumerate(updated_brg):
            item['Nomor'] = i + 1

        with open('barang.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_brg)
    except:
        print("=========================")
        print("Harus Angka!")
        print("=========================")

#function untuk menampilkan tabel user
def tampil_user():
    try:
        with open('user.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            users = list(reader)

            if len(users) == 0:
                print("Data Tidak Ditemukan!")
                return
            
            header = users[0]
            tabel = PrettyTable(header)

            for user in users[1:]:
                tabel.add_row(user)
            tabel.padding_width = 5

            print(tabel)
    except:
        print("=========================")
        print("Data Tidak Ditemukan")
        print("=========================")

#funtion untuk menambahkan saldo
def input_saldo():
    try:
        tampil_user()
        id_user = int(input("Masukkan ID pengguna : "))

        with open('user.csv', 'r') as csvfile:
            user = list(csv.DictReader(csvfile))

            for users in user:
                if id_user == int(users['ID']):
                    tambah = float(input("Masukkan jumlah saldo yang ingin ditambahkan : "))
                    if tambah > 0:
                        users['Saldo'] = float(users['Saldo']) + tambah
                        print("Saldo Behasil Ditambah!")
                        break
                    else:
                        print("=========================")
                        print("Input Harus Lebih Dari 0!")
                        print("=========================")
            else:
                print("=========================")
                print("Data Tidak Valid!")
                print("=========================")

            with open('user.csv', 'w', newline='') as csvfile:
                fieldnames = ['ID', 'Username', 'Password', 'Role', 'Saldo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(user)

    except:
        print("=========================")
        print("Harus Angka!")
        print("=========================")

#function untuk membeli barang yang ada di table barang
def transaksi():
    tampil_brg()
    total = 0
    keranjang = []

    while True:
        try:
            no_brg = int(input("Masukkan nomor barang yang ingin dibeli (ketik 0 untuk selesai) : "))
            if no_brg == 0:
                break

            with open('barang.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                brg = list(reader)

            for item in brg:
                if no_brg == int(item['Nomor']) and int(item['Stok']) > 0:
                    jml = int(input(f"Masukkan jumlah {item['Nama Barang']} yang ingin dibeli : "))
                    if jml > 0 and jml <= int(item['Stok']):
                        total += float(item['Harga']) * jml
                        keranjang.append({'Nama Barang' : item['Nama Barang'], 'Jumlah' : jml, 'Harga Satuan' : float(item['Harga'])})
                        if saldo > 0:
                            item['Stok'] = str(int(item['Stok']) - jml)
                            print("Barang berhasil ditembahkan ke keranjang!")
                            update_stok_brg(brg)
                        else:
                            print("Saldo Tidak Mencukupi!")
                            break
                    else:
                        print("=========================")
                        print("Jumlah Tidak Valid atau Melebihi Stok!")
                        print("=========================")
                    break
            else:
                print("=========================")
                print("Barang Tidak Ditemukan atau Stok Habis!")
                print("=========================")

        except ValueError:
            print("=========================")
            print("Harus Angka!")
            print("=========================")

    return keranjang, total

#function Struck
def invoice(id, keranjang, total):
    if keranjang:
        invoice_number = brg_auto() + 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = 0

        with open('invoice.csv', 'a', newline='') as csvfile:
            fieldnames = ['Invoice Number', 'User ID', 'Tanggal', 'Nama Barang', 'Jumlah', 'Harga Satuan']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for item in keranjang:
                total += item['Jumlah'] * item['Harga Satuan']
                writer.writerow({'Invoice Number': invoice_number, 'User ID': id, 'Tanggal': current_time,
                                'Nama Barang': item['Nama Barang'], 'Jumlah': item['Jumlah'],
                                'Harga Satuan': item['Harga Satuan']})

        with open('user.csv', 'r') as csvfile:
            users = list(csv.DictReader(csvfile))

        for user in users:
            if int(user['ID']) == id:
                if float(user['Saldo']) >= total:
                    user['Saldo'] = str(float(user['Saldo']) - total)
                    with open('user.csv', 'w', newline='') as csvfile:
                        fieldnames = ['ID', 'Username', 'Password', 'Role', 'Saldo']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(users)

                    tabel = PrettyTable(['Nama Barang', 'Jumlah', 'Harga Satuan', 'Total Harga'])
                    for item in keranjang:
                        subtotal = item['Jumlah'] * item['Harga Satuan']
                        tabel.add_row([item['Nama Barang'], item['Jumlah'], item['Harga Satuan'], subtotal])

                    print("\n==================================================")
                    print("Invoice : ")
                    print("Invoice Number : ", invoice_number)
                    print("User ID : ", id)
                    print("Tanggal : ", current_time)
                    print(tabel)
                    print("Total Harga : ", total)
                    print("Sisa Saldo : ", user['Saldo'])
                    print("==================================================")
                else:
                    print("Saldo Tidak Mencukupi untuk Melakukan Pembelian!")
                break
    else:
        print("=========================")
        print("Tidak ada barang yang dibeli.")
        print("=========================")

#function sort harga murah ke mahal
def sort_harga_murah(ascending=True):
    with open('barang.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        barang = list(reader)
        
        sorted_barang = sorted(barang, key=lambda x: float(x['Harga']), reverse=not ascending)
        
        with open('barang.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_barang)

        print("Barang berhasil diurutkan berdasarkan harga!")

#function sort harga mahal ke murah
def sort_harga_mahal(ascending=False):
    with open('barang.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        barang = list(reader)
        
        sorted_barang = sorted(barang, key=lambda x: float(x['Harga']), reverse=ascending)
        
        with open('barang.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_barang)

        print("Barang berhasil diurutkan berdasarkan harga!")

#function sort angka sesuai urutan
def sort_nomor(ascending=True):
    with open('barang.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        barang = list(reader)
        
        sorted_barang = sorted(barang, key=lambda x: float(x['Nomor']), reverse=not ascending)
        
        with open('barang.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nomor', 'Nama Barang', 'Harga', 'Stok']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_barang)

#function search
def cari():
    while True:
        keyword = input("Cari sesuai nomor barang (Untuk berhenti ketik '/selesai'): ")
        if keyword == "/selesai":
            break
        else:
            with open('barang.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

                results = []
                for item in data:
                    if keyword in item['Nomor']:
                        results.append(item)
                if not results:
                    print("No items found.")
                else:
                    header = data[0].keys()
                    table = PrettyTable(header)
                    for row in results:
                        table.add_row(row.values())
                    print(table)

#body
while True:
    #menu utama
    tampil_brg()
    print("Koperasi Sekolah")
    print("1. Registrasi")
    print("2. Login")
    print("3. Keluar")
    print("=========================")
    try:
        pilih = int(input("Pilih menu : "))
        if pilih == 1:
            register()
        elif pilih == 2:
            id, username, role, saldo = login()
            if role == 1:
                while True:
                    #menu admin
                    print("\nSelamat Datang Admin", username)
                    print("\n=========================")
                    print("Menu Admin")
                    print("1. Edit tabel")
                    print("2. Top-Up")
                    print("3. Logout")
                    print("=========================")
                    try:
                        pilih = int(input("Pilih Menu : "))
                        if pilih == 1:
                            while True:
                                #menu admin untuk edit tabel
                                tampil_brg()
                                print("Menu Edit Tabel")
                                print("1. Tambah Barang")
                                print("2. Edit Barang")
                                print("3. Hapus Barang")
                                print("4. Kembali")
                                print("=========================")
                                try:
                                    pilih = int(input("Pilih Menu : "))
                                    if pilih == 1:
                                        input_brg()
                                    elif pilih == 2:
                                        update_brg()
                                    elif pilih == 3:
                                        delete_brg()
                                    elif pilih == 4:
                                        break
                                    else:
                                        print("=========================")
                                        print("Data Tidak Valid!")
                                        print("=========================")
                                except:
                                    print("=========================")
                                    print("Harus Angka!")
                                    print("=========================")
                        elif pilih == 2:
                            while True:
                                #menu admin untuk top-upkan user
                                tampil_user()
                                print("Menu Top-Up")
                                print("1. Tambah Saldo")
                                print("2. Kembali")
                                print("=========================")
                                try:
                                    pilih = int(input("Masukkan pilihan anda : "))
                                    if pilih == 1:
                                        input_saldo()
                                    elif pilih == 2:
                                        break
                                    else:
                                        print("=========================")
                                        print("Data Tidak Valid!")
                                        print("=========================")
                                except:
                                    print("=========================")
                                    print("Harus Angka!")
                                    print("=========================")
                        elif pilih == 3:
                            break   
                        else:
                            print("=========================")
                            print("Data Tidak Valid!")   
                            print("=========================")
                    except:
                        print("=========================")
                        print("Harus Angka!")  
                        print("=========================")    
            elif role == 0:
                while True:
                    #menu user biasa
                    tampil_brg()
                    print("\nSelamat Datang", username)
                    print("\n=========================")
                    print("Menu Murid")
                    print("1. Cari Barang")
                    print("2. Beli Barang")
                    print("3. Sort (Murah --> Mahal)")
                    print("4. Sort (Mahal --> Murah)")
                    print("5. Logout")
                    print("=========================")
                    try:
                        pilih = int(input("Pilih menu : "))
                        if pilih == 1:
                            cari()
                        elif pilih == 2:
                            print("=========================")
                            print("Saldo : ", saldo)
                            keranjang, total = transaksi()
                            invoice(id, keranjang, total)
                        elif pilih == 3:
                            sort_harga_murah()
                        elif pilih == 4:
                            sort_harga_mahal(ascending=True)
                        elif pilih == 5:
                            sort_nomor()
                            break
                        else:
                            print("=========================")
                            print("Data Tidak Valid!")
                            print("=========================")
                    except:
                        print("=========================")
                        print("Harus Angka!")
                        print("=========================")
            elif pilih == 3:
                break
            else:
                print("=========================")
                print("Role Tidak Ditemukan!")
                print("=========================")
        elif pilih == 3:
            break
        else:
            print("=========================")
            print("Data Tidak Valid")
            print("=========================")
    except:
        print("=========================")
        print("Harus Angka!")
        print("=========================")