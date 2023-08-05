
# About
The Python Package Index Project (pypipr)

pypi : https://pypi.org/project/pypipr


# Setup
Install with pip
```
python -m pip install pypipr
```

Import with * for fastest access
```python
from pypipr.pypipr import *
```

# CONSTANT

`LINUX`

`WINDOWS`

# FUNCTION

## avg

`avg`

Simple Average Function karena tidak disediakan oleh python  

```python  
n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]  
print(avg(n))  
```

Output:
```py
16.285714285714285
```

## basename

`basename`

Mengembalikan nama file dari path  

```python  
print(basename("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
file.py
```

## batchmaker

`batchmaker`

Alat Bantu untuk membuat teks yang berulang.  
Gunakan {[start][separator][finish]([separator][step])}.  
```  
[start] dan [finish]    -> bisa berupa huruf maupun angka  
([separator][step])     -> bersifat optional  
[separator]             -> selain huruf dan angka  
[step]                  -> berupa angka positif  
```  

```python  
s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."  
print(generator.batchmaker(s))  
print(batchmaker(s))  
```

Output:
```py
<generator object generator.batchmaker at 0x00000211ED465190>
('Urutan 1 dan 10 dan j dan Z saja.', 'Urutan 1 dan 10 dan j dan K saja.', 'Urutan 1 dan 10 dan k dan Z saja.', 'Urutan 1 dan 10 dan k dan K saja.', 'Urutan 1 dan 9 dan j dan Z saja.', 'Urutan 1 dan 9 dan j dan K saja.', 'Urutan 1 dan 9 dan k dan Z saja.', 'Urutan 1 dan 9 dan k dan K saja.', 'Urutan 4 dan 10 dan j dan Z saja.', 'Urutan 4 dan 10 dan j dan K saja.', 'Urutan 4 dan 10 dan k dan Z saja.', 'Urutan 4 dan 10 dan k dan K saja.', 'Urutan 4 dan 9 dan j dan Z saja.', 'Urutan 4 dan 9 dan j dan K saja.', 'Urutan 4 dan 9 dan k dan Z saja.', 'Urutan 4 dan 9 dan k dan K saja.')
```

## calculate

`calculate`

Mengembalikan hasil dari perhitungan teks menggunakan modul pint.  
Mendukung perhitungan matematika dasar dengan satuan.  

Return value:  
- Berupa class Quantity dari modul pint  

Format:  
- f"{result:~P}"            -> pretty  
- f"{result:~H}"            -> html  
- result.to_base_units()    -> SI  
- result.to_compact()       -> human readable  

```python  
fx = "3 meter * 10 cm * 3 km"  
res = calculate(fx)  
print(res)  
print(res.to_base_units())  
print(res.to_compact())  
print(f"{res:~P}")  
print(f"{res:~H}")  
```

Output:
```py
90 centimeter * kilometer * meter
900.0 meter ** 3
900.0 meter ** 3
90 cm·km·m
90 cm km m
```

## chunck_array

`chunck_array`

Membagi array menjadi potongan-potongan dengan besaran yg diinginkan  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(generator.chunck_array(array, 5))  
print(chunck_array(array, 5))  
```

Output:
```py
<generator object generator.chunck_array at 0x00000211ED4650B0>
([2, 3, 12, 3, 3], [42, 42, 1, 43, 2], [42, 41, 4, 24, 32], [42, 3, 12, 32, 42], [42])
```

## console_run

`console_run`

Menjalankan command seperti menjalankan command di Command Terminal  

```py  
console_run('dir')  
console_run('ls')  
```

## create_folder

`create_folder`

Membuat folder.  
Membuat folder secara recursive dengan permission.  

```py  
create_folder("contoh_membuat_folder")  
create_folder("contoh/membuat/folder/recursive")  
create_folder("./contoh_membuat_folder/secara/recursive")  
```

## datetime_from_string

`datetime_from_string`

Parse iso_string menjadi datetime object  

```python  
print(datetime_from_string("2022-12-12 15:40:13").isoformat())  
print(datetime_from_string("2022-12-12 15:40:13", timezone="Asia/Jakarta").isoformat())  
```

Output:
```py
2022-12-12T15:40:13+00:00
2022-12-12T15:40:13+07:00
```

## datetime_now

`datetime_now`

Memudahkan dalam membuat Datetime untuk suatu timezone tertentu  

```python  
print(datetime_now("Asia/Jakarta"))  
print(datetime_now("GMT"))  
print(datetime_now("Etc/GMT+7"))  
```

Output:
```py
2023-06-04 21:11:06.900586+07:00
2023-06-04 14:11:06.901586+00:00
2023-06-04 07:11:06.903739-07:00
```

## dict_first

`dict_first`

Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.  

```python  
d = {  
    "key2": "value2",  
    "key3": "value3",  
    "key1": "value1",  
}  
print(dict_first(d, remove=True))  
print(dict_first(d))  
```

Output:
```py
('key2', 'value2')
('key3', 'value3')
```

## dirname

`dirname`

Mengembalikan nama folder dari path.  
Tanpa trailing slash di akhir.  

```python  
print(dirname("/ini/nama/folder/ke/file.py"))  
```

Output:
```py
/ini/nama/folder/ke
```

## exit_if_empty

`exit_if_empty`

Keluar dari program apabila seluruh variabel  
setara dengan empty  

```py  
var1 = None  
var2 = '0'  
exit_if_empty(var1, var2)  
```

## explode

`explode`

Memecah text menjadi list berdasarkan separator.  

```python  
t = '/ini/contoh/path/'  
print(explode(t, separator='/'))  
```

Output:
```py
['', 'ini', 'contoh', 'path', '']
```

## filter_empty

`filter_empty`

## get_class_method

`get_class_method`

Mengembalikan berupa tuple yg berisi list dari method dalam class  

```python  
class ExampleGetClassMethod:  
    def a():  
        return [x for x in range(10)]  

    def b():  
        return [x for x in range(10)]  

    def c():  
        return [x for x in range(10)]  

    def d():  
        return [x for x in range(10)]  

print(get_class_method(ExampleGetClassMethod))  
```

Output:
```py
(<function ExampleGetClassMethod.a at 0x00000211ED622CA0>, <function ExampleGetClassMethod.b at 0x00000211ED622C10>, <function ExampleGetClassMethod.c at 0x00000211ED622D30>, <function ExampleGetClassMethod.d at 0x00000211ED622DC0>)
```

## get_filemtime

`get_filemtime`

Mengambil informasi last modification time file dalam nano seconds  

```python  
print(get_filemtime(__file__))  
```

Output:
```py
1685887788168658300
```

## get_filesize

`get_filesize`

Mengambil informasi file size dalam bytes  

```python  
print(get_filesize(__file__))  
```

Output:
```py
41866
```

## github_pull

`github_pull`

Menjalankan command `git pull`  

```py  
github_pull()  
```

## github_push

`github_push`

Menjalankan command status, add, commit dan push  

```py  
github_push('Commit Message')  
```

## iexec

`iexec`

improve exec() python function untuk mendapatkan outputnya  

```python  
print(iexec('print(9*9)'))  
```

Output:
```py
81

```

## implode

`implode`

Simplify Python join functions like PHP function.  
Iterable bisa berupa sets, tuple, list, dictionary.  

```python  
arr = {'asd','dfs','weq','qweqw'}  
print(implode(arr, ', '))  

arr = '/ini/path/seperti/url/'.split('/')  
print(implode(arr, ','))  
print(implode(arr, ',', remove_empty=True))  

arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}  
print(implode(arr, separator='</li>\n<li>', start='<li>', end='</li>', recursive_flat=True))  
print(implode(arr, separator='</div>\n<div>', start='<div>', end='</div>'))  
print(implode(10, ' '))  
```

Output:
```py
qweqw, asd, dfs, weq
,ini,path,seperti,url,
ini,path,seperti,url
<li>satu</li>
<li>12</li>
<li>34</li>
<li>56</li>
<li>tiga</li>
<li>empat</li>
<div>satu</div>
<div><div>12</div>
<div>34</div>
<div>56</div></div>
<div>tiga</div>
<div>empat</div>
10
```

## input_char

`input_char`

Meminta masukan satu huruf tanpa menekan Enter.  

```py  
input_char("Input char : ")  
input_char("Input char : ", default='Y')  
input_char("Input Char without print : ", echo_char=False)  
```

## iopen

`iopen`

Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.  

Baca File :  
- Membaca seluruh file.  
- Jika berhasil content dapat diparse dengan regex.  
- Apabila File berupa html, dapat diparse dengan css atau xpath.  

Tulis File :  
- Menulis pada file.  
- Jika file tidak ada maka akan dibuat.  
- Jika file memiliki content maka akan di overwrite.  

Membaca URL :  
- Mengakses URL dan mengembalikan isi html nya berupa teks.  
- Content dapat diparse dengan regex, css atau xpath.  

Tulis URL :  
- Mengirimkan data dengan metode POST ke url.  
- Jika berhasil dan response memiliki content, maka dapat diparse dengan regex, css atau xpath.  


```python  
# FILE  
print(iopen("__iopen.txt", "mana aja"))  
print(iopen("__iopen.txt", regex="(\w+)"))  
# URL  
print(iopen("https://www.google.com/", css_select="a"))  
print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))  
```

Output:
```py
8
['mana', 'aja']
[<Element a at 0x211eaa6b590>, <Element a at 0x211ec8139f0>, <Element a at 0x211ed57c270>, <Element a at 0x211ed498cc0>, <Element a at 0x211ed5a0540>, <Element a at 0x211ed5a08b0>, <Element a at 0x211ed5a09f0>, <Element a at 0x211ed5a0a40>, <Element a at 0x211ed5a0b30>, <Element a at 0x211ed5a0ae0>, <Element a at 0x211ed5a06d0>, <Element a at 0x211ed5a0cc0>, <Element a at 0x211ed5a0d10>, <Element a at 0x211ed5a0b80>, <Element a at 0x211ed5a0ea0>, <Element a at 0x211ed5a0ef0>, <Element a at 0x211ed5a0e50>, <Element a at 0x211ec5fd090>]
False
```

## irange

`irange`

Improve python range() function untuk pengulangan menggunakan huruf  

```python  
print(generator.irange('a', 'z'))  
print(irange('H', 'a'))  
print(irange('1', '5', 3))  
print(irange('1', 5, 3))  
# print(irange('a', 5, 3))  
print(irange(-10, 4, 3))  
print(irange(1, 5))  
```

Output:
```py
<generator object generator.irange at 0x00000211ED465270>
['H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a']
['1', '4']
[1, 4]
[-10, -7, -4, -1, 2]
[1, 2, 3, 4, 5]
```

## is_empty

`is_empty`

Mengecek apakah variable setara dengan nilai kosong pada empty.  

Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk  
pengecekan lokasi memory yang sama menggunakan keyword 'is'  

```python  
print(is_empty("teks"))  
print(is_empty(True))  
print(is_empty(False))  
print(is_empty(None))  
print(is_empty(0))  
print(is_empty([]))  
```

Output:
```py
False
False
True
True
True
True
```

## is_iterable

`is_iterable`

Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak  

```python  
s = 'ini string'  
print(is_iterable(s))  

l = [12,21,2,1]  
print(is_iterable(l))  

r = range(100)  
print(is_iterable(r))  

d = {'a':1, 'b':2}  
print(is_iterable(d.values()))  
```

Output:
```py
False
True
True
True
```

## is_valid_url

`is_valid_url`

Mengecek apakah path merupakan URL yang valid atau tidak.  
Cara ini merupakan cara yang paling efektif.  

```python  
print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))  
print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))  
```

Output:
```py
True
True
```

## iscandir

`iscandir`

Mempermudah scandir untuk mengumpulkan folder dan file.  

```python  
print(generator.iscandir())  
print(iscandir("./", recursive=False, scan_file=False))  
```

Output:
```py
<generator object generator.iscandir at 0x00000211ED465270>
(WindowsPath('.git'), WindowsPath('.pytest_cache'), WindowsPath('.vscode'), WindowsPath('dist'), WindowsPath('pypipr'))
```

## log

`log`

Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada.  
Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.  

```py  
@log  
def some_function():  
    pass  

@log()  
def some_function_again():  
    pass  

@log("Calling some function")  
def some_function_more():  
    pass  

some_function()  
some_function_again()  
some_function_more()  
```

## print_colorize

`print_colorize`

Print text dengan warna untuk menunjukan text penting  

```py  
print_colorize("Print some text")  
print_colorize("Print some text", color=colorama.Fore.RED)  
```

## print_dir

`print_dir`

Print property dan method yang tersedia pada variabel  

```python  
p = pathlib.Path("https://www.google.com/")  
print_dir(p, colorize=False)  
```

Output:
```py
           __bytes__ : b'https:\\www.google.com'
           __class__ : .
             __dir__ : ['__module__', '__doc__', '__slots__', 'is_mount', '__new__', '_init', '_make_child_relpath', '__enter__', '__exit__', '_opener', '_raw_open', 'cwd', 'home', 'samefile', 'iterdir', 'glob', 'rglob', 'absolute', 'resolve', 'stat', 'owner', 'group', 'open', 'read_bytes', 'read_text', 'write_bytes', 'write_text', 'readlink', 'touch', 'mkdir', 'chmod', 'lchmod', 'unlink', 'rmdir', 'lstat', 'link_to', 'rename', 'replace', 'symlink_to', 'exists', 'is_dir', 'is_file', 'is_symlink', 'is_block_device', 'is_char_device', 'is_fifo', 'is_socket', 'expanduser', '_accessor', '__reduce__', '_parse_args', '_from_parts', '_from_parsed_parts', '_format_parsed_parts', '_make_child', '__str__', '__fspath__', 'as_posix', '__bytes__', '__repr__', 'as_uri', '_cparts', '__eq__', '__hash__', '__lt__', '__le__', '__gt__', '__ge__', '__class_getitem__', 'drive', 'root', 'anchor', 'name', 'suffix', 'suffixes', 'stem', 'with_name', 'with_stem', 'with_suffix', 'relative_to', 'is_relative_to', 'parts', 'joinpath', '__truediv__', '__rtruediv__', 'parent', 'parents', 'is_absolute', 'is_reserved', 'match', '_cached_cparts', '_drv', '_hash', '_parts', '_pparts', '_root', '_str', '__getattribute__', '__setattr__', '__delattr__', '__ne__', '__init__', '__reduce_ex__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__', '_flavour']
             __doc__ : Path subclass for Windows systems.

    On a Windows system, instantiating a Path should return this object.
    
           __enter__ : https:\www.google.com
          __fspath__ : https:\www.google.com
            __hash__ : -8424695270096760017
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.WindowsPath'>, ('https:', 'www.google.com'))
            __repr__ : WindowsPath('https:/www.google.com')
          __sizeof__ : 80
           __slots__ : ()
             __str__ : https:\www.google.com
    __subclasshook__ : NotImplemented
           _accessor : <pathlib._NormalAccessor object at 0x00000211EC83D040>
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._WindowsFlavour object at 0x00000211EC8317F0>
               _hash : -8424695270096760017
               _init : None
              _parts : ['https:', 'www.google.com']
               _root : 
                _str : https:\www.google.com
            absolute : C:\Users\ToshibaM840\Desktop\website\pypipr\https:\www.google.com
              anchor : 
            as_posix : https:/www.google.com
                 cwd : C:\Users\ToshibaM840\Desktop\website\pypipr
               drive : 
          expanduser : https:\www.google.com
                home : C:\Users\ToshibaM840
         is_absolute : False
         is_reserved : False
             iterdir : <generator object Path.iterdir at 0x00000211ED451900>
            joinpath : https:\www.google.com
                name : www.google.com
              parent : https:
             parents : <WindowsPath.parents>
               parts : ('https:', 'www.google.com')
                root : 
                stem : www.google
              suffix : .com
            suffixes : ['.google', '.com']
```

## print_log

`print_log`

Akan melakukan print ke console.  
Berguna untuk memberikan informasi proses program yg sedang berjalan.  

```py  
print_log("Standalone Log")  
```

## random_bool

`random_bool`

Menghasilkan nilai random True atau False.  
Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.  
Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  

```python  
print(random_bool())  
```

Output:
```py
False
```

## serialize

`serialize`

Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.  
String yang dihasilkan berbentuk syntax YAML/JSON/HTML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42]),  
}  
print(serialize(data))  
print(serialize(data, syntax='html'))  
```

Output:
```py
a: 123
l: !!python/tuple
- 12
- 23
-   - 12
    - 42
t:
- disini
- senang
- disana
- senang

<table>
    <tbody>
        <tr>
            <th>a</th>
            <td>
                <span>123</span>
            </td>
        </tr>
        <tr>
            <th>t</th>
            <td>
                <ul>
                    <li>
                        <span>disini</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                    <li>
                        <span>disana</span>
                    </li>
                    <li>
                        <span>senang</span>
                    </li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>l</th>
            <td>
                <ul>
                    <li>
                        <span>12</span>
                    </li>
                    <li>
                        <span>23</span>
                    </li>
                    <li>
                        <ul>
                            <li>
                                <span>12</span>
                            </li>
                            <li>
                                <span>42</span>
                            </li>
                        </ul>
                    </li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

```

## serialize_html

`serialize_html`

Serialisasi python variabel menjadi HTML.  
```  
List -> <ul>...</ul>  
Dict -> <table>...</table>  
```  

```python  
data = {  
    'abc': 123,  
    'list': [1, 2, 3, 4, 5],  
    'dict': {'a': 1, 'b':2, 'c':3},  
}  
print(serialize_html(data))  
```

Output:
```py
<table>
  <tbody>
    <tr>
      <th>abc</th>
      <td>
        <span>123</span>
      </td>
    </tr>
    <tr>
      <th>list</th>
      <td>
        <ul>
          <li>
            <span>1</span>
          </li>
          <li>
            <span>2</span>
          </li>
          <li>
            <span>3</span>
          </li>
          <li>
            <span>4</span>
          </li>
          <li>
            <span>5</span>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <th>dict</th>
      <td>
        <table>
          <tbody>
            <tr>
              <th>a</th>
              <td>
                <span>1</span>
              </td>
            </tr>
            <tr>
              <th>b</th>
              <td>
                <span>2</span>
              </td>
            </tr>
            <tr>
              <th>c</th>
              <td>
                <span>3</span>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>

```

## set_timeout

`set_timeout`

Menjalankan fungsi ketika sudah sekian detik.  
Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka  
program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,  
kemudian program dihentikan.  

```python  
set_timeout(3, lambda: print("Timeout 3"))  
x = set_timeout(7, lambda: print("Timeout 7"))  
print(x)  
print("menghentikan timeout 7")  
x.cancel()  
```

Output:
```py
<Timer(Thread-2, started 14244)>
menghentikan timeout 7
```

## sets_ordered

`sets_ordered`

Hanya mengambil nilai unik dari suatu list  

```python  
array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]  
print(generator.sets_ordered(array))  
print(sets_ordered(array))  
```

Output:
```py
<generator object generator.sets_ordered at 0x00000211ED4517B0>
[2, 3, 12, 42, 1, 43, 41, 4, 24, 32]
```

## str_cmp

`str_cmp`

Membandingakan string secara incase-sensitive menggunakan lower().  
Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().  
perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan  
overhead yg besar.  
```python  
print(str_cmp('teks1', 'Teks1'))  
```

Output:
```py
True
```

## strtr

`strtr`

STRing TRanslate mengubah string menggunakan kamus dari dict.  
Replacement dapat berupa text biasa ataupun regex pattern.  
Apabila replacement berupa regex, gunakan raw string `r"..."`  
Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya gunakan `\1`, `\2`, .., dst.  

```python  
text = 'aku ini mau ke sini'  
replacements = {  
    "sini": "situ",  
    r"(ini)": r"itu dan \1",  
}  
print(strtr(text, replacements))  
```

Output:
```py
aku itu dan ini mau ke situ
```

## to_str

`to_str`

Mengubah value menjadi string literal  

```python  
print(to_str(5))  
print(to_str([]))  
print(to_str(False))  
print(to_str(True))  
print(to_str(None))  
```

Output:
```py
5

False
True

```

## unserialize

`unserialize`

Mengubah string data hasil dari serialize menjadi variabel.  
String data adalah berupa syntax YAML.  

```python  
data = {  
    'a': 123,  
    't': ['disini', 'senang', 'disana', 'senang'],  
    'l': (12, 23, [12, 42])  
}  
s = serialize(data)  
print(unserialize(s))  
```

## unserialize_html

`unserialize_html`

Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html  
dan menjadikannya data python berupa list.  
setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.  
```  
list (<ul>)     -> list         -> list satu dimensi  
table (<table>) -> list[list]   -> list satu dimensi didalam list  
```  

```python  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [['Harga Emas Hari Ini - Minggu, 04 Juni 2023'],
  ['Spot Emas USD↓1.948,20 (-5,06) / oz',
   'Kurs IDR15.140,00 / USD',
   'Emas IDR↓948.310 (-2.463) / gr'],
  ['LM Antam (Jual)1.057.000 / gr', 'LM Antam (Beli)943.000 / gr']],
 [['Harga Emas Hari Ini'],
  ['Gram', 'Gedung Antam Jakarta', 'Pegadaian'],
  ['per Gram (Rp)', 'per Batangan (Rp)', 'per Gram (Rp)', 'per Batangan (Rp)'],
  ['1000',
   '998',
   '997.600',
   '1.022.540 (-3.075)',
   '1.022.540.000 (-3.075.000)'],
  ['500', '1.995', '997.640', '1.022.582 (-3.074)', '511.291.000 (-1.537.000)'],
  ['250', '3.992', '998.060', '1.023.012 (-3.076)', '255.753.000 (-769.000)'],
  ['100', '9.991', '999.120', '1.024.100 (-3.080)', '102.410.000 (-308.000)'],
  ['50', '19.998', '999.900', '1.024.900 (-3.080)', '51.245.000 (-154.000)'],
  ['25', '40.059', '1.001.480', '1.026.520 (-3.080)', '25.663.000 (-77.000)'],
  ['10', '100.650', '1.006.500', '1.031.700 (-3.100)', '10.317.000 (-31.000)'],
  ['5', '202.400', '1.012.000', '1.037.400 (-3.000)', '5.187.000 (-15.000)'],
  ['3', '339.556', '1.018.667', '1.044.333 (-3.000)', '3.133.000 (-9.000)'],
  ['2', '513.500', '1.027.000', '1.053.000 (-3.000)', '2.106.000 (-6.000)'],
  ['1', '1.057.000', '1.057.000', '1.084.000 (-3.000)', '1.084.000 (-3.000)'],
  ['0.5', '2.314.000', '1.157.000', '1.188.000 (-2.000)', '594.000 (-1.000)'],
  ['Update harga LM Antam :04 Juni 2023, pukul 06:06Harga pembelian kembali '
   ':Rp. 943.000/gram',
   'Update harga LM Pegadaian :03 Juni 2023']],
 [['Spot Harga Emas Hari Ini (Market Close)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '1.948,20 (-5,06)', '15.140,00', '29.495.748'],
  ['Gram\xa0(gr)', '62,64', '15.140,00', '948.310 (-2.463)'],
  ['Kilogram\xa0(kg)', '62.636,08', '15.140,00', '948.310.320'],
  ['Update harga emas :04 Juni 2023, pukul 21:11Update kurs :13 Febuari 2023, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100', '96.985.000', '969.850', '94.800.000', '948.000'],
  ['50', '48.545.000', '970.900', '47.400.000', '948.000'],
  ['25', '24.375.000', '975.000', '23.700.000', '948.000'],
  ['10', '9.800.000', '980.000', '9.480.000', '948.000'],
  ['5', '4.952.000', '990.400', '4.740.000', '948.000'],
  ['1', '1.023.000', '1.023.000', '948.000', '948.000'],
  ['', 'Update :31 Mei 2023, pukul 11:52']],
 [['Konversi Satuan'],
  ['Satuan', 'Ounce (oz)', 'Gram (gr)', 'Kilogram (kg)'],
  ['Ounce\xa0(oz)', '1', '31,1034767696', '0,0311034768'],
  ['Gram\xa0(gr)', '0,0321507466', '1', '0.001'],
  ['Kilogram\xa0(kg)', '32,1507466000', '1.000', '1']],
 [['Pergerakan Harga Emas Dunia'],
  ['Waktu', 'Emas'],
  ['Unit', 'USD', 'IDR'],
  ['Angka', '+/-', 'Angka', '+/-'],
  ['Hari Ini', 'Kurs', '', '', '15.140', '%'],
  ['oz', '1.953,26', '-5,06-0,26%', '29.572.356', '-76.608-0,26%'],
  ['gr', '62,80', '-0,16-0,26%', '950.773', '-2.463-0,26%'],
  ['30 Hari', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.017,73', '-69,53-3,45%', '30.548.432', '-1.052.684-3,45%'],
  ['gr', '64,87', '-2,24-3,45%', '982.155', '-33.845-3,45%'],
  ['2 Bulan', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.020,58', '-72,38-3,58%', '30.591.581', '-1.095.833-3,58%'],
  ['gr', '64,96', '-2,33-3,58', '983.542', '-35.232-3,58%'],
  ['6 Bulan', 'Kurs', '', '', '15.409', '-269-1,75%'],
  ['oz', '1.772,05', '+176,15+9,94%', '27.305.518', '+2.190.230+8,02%'],
  ['gr', '56,97', '+5,66+9,94%', '877.893', '+70.418+8,02%'],
  ['1 Tahun', 'Kurs', '', '', '14.526', '+614+4,23%'],
  ['oz', '1.851,10', '+97,10+5,25%', '26.889.079', '+2.606.669+9,69%'],
  ['gr', '59,51', '+3,12+5,25%', '864.504', '+83.806+9,69%'],
  ['2 Tahun', 'Kurs', '', '', '14.297', '+843+5,90%'],
  ['oz', '1.889,32', '+58,88+3,12%', '27.011.627', '+2.484.121+9,20%'],
  ['gr', '60,74', '+1,89+3,12%', '868.444', '+79.866+9,20%'],
  ['3 Tahun', 'Kurs', '', '', '14.165', '+975+6,88%'],
  ['oz', '1.717,65', '+230,55+13,42%', '24.330.529', '+5.165.219+21,23%'],
  ['gr', '55,22', '+7,41+13,42%', '782.245', '+166.066+21,23%'],
  ['5 Tahun', 'Kurs', '', '', '13.887', '+1.253+9,02%'],
  ['oz', '1.298,48', '+649,72+50,04%', '18.031.992', '+11.463.756+63,57%'],
  ['gr', '41,75', '+20,89+50,04%', '579.742', '+368.568+63,57%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '62,64↓', '%'],
  ['KURS', '14.901,90↓', '%'],
  ['IDR', '933.396,67↓', '%'],
  ['Minggu, 04 Juni 2023 21:11']],
 [[''],
  ['Emas 1 Gram (IDR)Emas 1 Gram (USD)Kurs USD-IDR',
   'Hari Ini',
   '1 Bulan',
   '1 Tahun',
   '5 Tahun',
   'Max',
   '']],
 [['Pergerakkan Harga Emas 1 Gram'],
  ['', 'Penutupan Kemarin', 'Pergerakkan Hari Ini', 'Rata-rata'],
  ['USD', '62,64', '62,64 - 62,64', '62,64'],
  ['KURS', '14.901,90', '14.901,90 - 14.901,90', '14.901,90'],
  ['IDR', '933.396,67', '933.396,67 - 933.396,67', '933.396,67'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '58,64', '58,23 - 65,97', '+4,00 (6,82%)'],
  ['KURS', '15.538,50', '14.669,40 - 15.629,15', '-636,60(-4,10%)'],
  ['IDR', '911.153,72', '888.842,84 - 982.694,10', '+22.242,95 (2,44%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '59,50', '52,31 - 65,97', '+3,14 (5,28%)'],
  ['KURS', '14.432,40', '14.431,75 - 15.785,40', '+469,50 (3,25%)'],
  ['IDR', '858.687,49', '795.009,21 - 982.694,10', '+74.709,18 (8,70%)']])
```

# CLASS

## ComparePerformance

`ComparePerformance`

Menjalankan seluruh method dalam class,  
Kemudian membandingkan waktu yg diperlukan.  
Nilai 100 berarti yang tercepat.  
  
```python  
class ExampleComparePerformance(ComparePerformance):  
    # number = 1  
    z = 10  
  
    def a(self):  
        return (x for x in range(self.z))  
  
    def b(self):  
        return tuple(x for x in range(self.z))  
  
    def c(self):  
        return [x for x in range(self.z)]  
  
    def d(self):  
        return list(x for x in range(self.z))  
  
pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
print(ExampleComparePerformance().compare_performance())  
```

Output:
```py
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x00000211ED451BA0>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 109, 'b': 129, 'c': 100, 'd': 151}
{'a': 100, 'b': 123, 'c': 100, 'd': 150}
{'a': 103, 'b': 133, 'c': 100, 'd': 155}
{'a': 100, 'b': 140, 'c': 104, 'd': 164}
{'a': 100, 'b': 145, 'c': 108, 'd': 162}
```

## RunParallel

`RunParallel`

Menjalankan program secara bersamaan.  
  
- `class RunParallel` didesain hanya untuk pemrosesan data saja.  
- Penggunaannya `class RunParallel` dengan cara membuat instance sub class beserta data yg akan diproses, kemudian panggil fungsi yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`, kemudian dapatkan hasilnya.  
- `class RunParallel` tidak didesain untuk menyimpan data, karena setiap module terutama module `multiprocessing` tidak dapat mengakses data kelas dari proses yg berbeda.  
- Semua methods akan dijalankan secara paralel kecuali method dengan nama yg diawali underscore `_`  
- Method untuk multithreading/multiprocessing harus memiliki 2 parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter `result` digunakan untuk memberikan return value dari method, dan Parameter `q` digunakan untuk mengirim data antar proses.  
- Method untuk asyncio harus menggunakan keyword `async def`, dan untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`, dan keyword `return` untuk memberikan return value.  
- Return Value berupa dictionary dengan key adalah nama function, dan value adalah return value dari setiap fungsi  
- Menjalankan Multiprocessing harus berada dalam blok `if __name__ == "__main__":` karena area global pada program akan diproses lagi. Terutama pada sistem operasi windows.  
- `run_asyncio()` akan menjalankan kode dalam satu program, hanya saja alur program dapat berpindah-pindah menggunkan `await asyncio.sleep(0)`.  
- `run_multi_threading()` akan menjalankan program dalam satu CPU, hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar berjalan secara bersamaan namun bisa meningkatkan kecepatan penyelesaian program, dan dapat saling mengakses resource antar program.  Akses resource antar program bisa secara langsung maupun menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
- `run_multi_processing()` akan menjalankan program dengan beberapa CPU. Program akan dibuatkan environment sendiri yang terpisah dari program induk. Keuntungannya adalah program dapat benar-benar berjalan bersamaan, namun tidak dapat saling mengakses resource secara langsung. Akses resource menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.  
  
```python  
class ExampleRunParallel(RunParallel):  
    z = "ini"  
  
    def __init__(self) -> None:  
        self.pop = random.randint(0, 100)  
  
    def _set_property_here(self, v):  
        self.prop = v  
  
    def a(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["a"] = "a"  
        q.put("from a 1")  
        q.put("from a 2")  
  
    def b(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["b"] = "b"  
        result["q_get"] = q.get()  
  
    def c(self, result: dict, q: queue.Queue):  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["c"] = "c"  
        result["q_get"] = q.get()  
  
    async def d(self):  
        print("hello")  
        await asyncio.sleep(0)  
        print("hello")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["d"] = "d"  
        return result  
  
    async def e(self):  
        print("world")  
        await asyncio.sleep(0)  
        print("world")  
  
        result = {}  
        result["z"] = self.z  
        result["pop"] = self.pop  
        result["e"] = "e"  
        return result  
  
if __name__ == "__main__":  
    print(ExampleRunParallel().run_asyncio())  
    print(ExampleRunParallel().run_multi_threading())  
    print(ExampleRunParallel().run_multi_processing())  
```

Output:
```py
```

## __calculate__quantity__

`__calculate__quantity__`

## generator

`generator`

Class ini menyediakan beberapa fungsi yang bisa mengembalikan generator.  
Digunakan untuk mengoptimalkan program.  
  
Class ini dibuat karena python generator yang disimpan dalam variabel  
hanya dapat diakses satu kali.
