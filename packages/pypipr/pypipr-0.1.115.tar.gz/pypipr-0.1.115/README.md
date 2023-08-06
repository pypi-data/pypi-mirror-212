
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
<generator object generator.batchmaker at 0x0000014075FE6190>
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
<generator object generator.chunck_array at 0x0000014075FE60B0>
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
2023-06-05 19:12:27.671717+07:00
2023-06-05 12:12:27.672714+00:00
2023-06-05 05:12:27.675718-07:00
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
(<function ExampleGetClassMethod.a at 0x000001407619FCA0>, <function ExampleGetClassMethod.b at 0x000001407619FC10>, <function ExampleGetClassMethod.c at 0x000001407619FD30>, <function ExampleGetClassMethod.d at 0x000001407619FDC0>)
```

## get_filemtime

`get_filemtime`

Mengambil informasi last modification time file dalam nano seconds  

```python  
print(get_filemtime(__file__))  
```

Output:
```py
1685966815090366000
```

## get_filesize

`get_filesize`

Mengambil informasi file size dalam bytes  

```python  
print(get_filesize(__file__))  
```

Output:
```py
43701
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
asd, weq, qweqw, dfs
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
[<Element a at 0x14076050ae0>, <Element a at 0x14075c850e0>, <Element a at 0x14076016900>, <Element a at 0x14076121b30>, <Element a at 0x14075f06720>, <Element a at 0x14075f064a0>, <Element a at 0x14075f06900>, <Element a at 0x14075f066d0>, <Element a at 0x140761005e0>, <Element a at 0x14076100b80>, <Element a at 0x140761006d0>, <Element a at 0x1407619b130>, <Element a at 0x140761bcdb0>, <Element a at 0x140761bcea0>, <Element a at 0x140761bc9f0>, <Element a at 0x140761bce00>, <Element a at 0x140761bce50>, <Element a at 0x140761bcef0>]
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
<generator object generator.irange at 0x0000014075FE6350>
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
<generator object generator.iscandir at 0x0000014075FE6350>
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
            __hash__ : -8589791309141689556
            __init__ : None
   __init_subclass__ : None
          __module__ : pathlib
          __reduce__ : (<class 'pathlib.WindowsPath'>, ('https:', 'www.google.com'))
            __repr__ : WindowsPath('https:/www.google.com')
          __sizeof__ : 80
           __slots__ : ()
             __str__ : https:\www.google.com
    __subclasshook__ : NotImplemented
           _accessor : <pathlib._NormalAccessor object at 0x00000140753BE1C0>
      _cached_cparts : ['https:', 'www.google.com']
             _cparts : ['https:', 'www.google.com']
                _drv : 
            _flavour : <pathlib._WindowsFlavour object at 0x00000140753B1A00>
               _hash : -8589791309141689556
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
             iterdir : <generator object Path.iterdir at 0x0000014075FD2890>
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
True
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
<Timer(Thread-2, started 19244)>
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
<generator object generator.sets_ordered at 0x0000014075FD2740>
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
apabila data berupa ul maka dapat dicek type(data) -> html_ul  
apabila data berupa ol maka dapat dicek type(data) -> html_ol  
apabila data berupa dl maka dapat dicek type(data) -> html_dl  
apabila data berupa table maka dapat dicek type(data) -> html_table  

```python  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/")), depth=10)  
pprint.pprint(unserialize_html(iopen("https://harga-emas.org/1-gram/")), depth=10)  
```

Output:
```py
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [['Harga Emas Hari Ini - Senin, 05 Juni 2023'],
  ['Spot Emas USD↓1.941,56 (-6,64) / oz',
   'Kurs IDR15.140,00 / USD',
   'Emas IDR↓945.078 (-3.232) / gr'],
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
  ['Update harga LM Antam :05 Juni 2023, pukul 08:29Harga pembelian kembali '
   ':Rp. 943.000/gram',
   'Update harga LM Pegadaian :03 Juni 2023']],
 [['Spot Harga Emas Hari Ini (Market Open)'],
  ['Satuan', 'USD', 'Kurs\xa0Dollar', 'IDR'],
  ['Ounce\xa0(oz)', '1.941,56 (-6,64)', '15.140,00', '29.395.218'],
  ['Gram\xa0(gr)', '62,42', '15.140,00', '945.078 (-3.232)'],
  ['Kilogram\xa0(kg)', '62.422,60', '15.140,00', '945.078.218'],
  ['Update harga emas :05 Juni 2023, pukul 19:12Update kurs :13 Febuari 2023, '
   'pukul 09:10']],
 [['Gram', 'UBS Gold 99.99%'],
  ['Jual', 'Beli'],
  ['/ Batang', '/ Gram', '/ Batang', '/ Gram'],
  ['100',
   '96.235.000 (-750.000)',
   '962.350 (-7.500)',
   '94.400.000 (-400.000)',
   '944.000 (-4.000)'],
  ['50',
   '48.170.000 (-375.000)',
   '963.400 (-7.500)',
   '47.200.000 (-200.000)',
   '944.000 (-4.000)'],
  ['25',
   '24.188.000 (-187.000)',
   '967.520 (-7.480)',
   '23.600.000 (-100.000)',
   '944.000 (-4.000)'],
  ['10',
   '9.725.000 (-75.000)',
   '972.500 (-7.500)',
   '9.440.000 (-40.000)',
   '944.000 (-4.000)'],
  ['5',
   '4.915.000 (-37.000)',
   '983.000 (-7.400)',
   '4.720.000 (-20.000)',
   '944.000 (-4.000)'],
  ['1',
   '1.016.000 (-7.000)',
   '1.016.000 (-7.000)',
   '944.000 (-4.000)',
   '944.000 (-4.000)'],
  ['', 'Update :05 Juni 2023, pukul 10:52']],
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
  ['oz', '1.948,20', '-6,64-0,34%', '29.495.748', '-100.530-0,34%'],
  ['gr', '62,64', '-0,21-0,34%', '948.310', '-3.232-0,34%'],
  ['30 Hari', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.016,87', '-75,31-3,73%', '30.535.412', '-1.140.193-3,73%'],
  ['gr', '64,84', '-2,42-3,73%', '981.736', '-36.658-3,73%'],
  ['2 Bulan', 'Kurs', '', '', '15.140', '%'],
  ['oz', '2.012,83', '-71,27-3,54%', '30.474.246', '-1.079.028-3,54%'],
  ['gr', '64,71', '-2,29-3,54', '979.770', '-34.692-3,54%'],
  ['6 Bulan', 'Kurs', '', '', '15.576', '-436-2,80%'],
  ['oz', '1.781,44', '+160,12+8,99%', '27.747.709', '+1.647.509+5,94%'],
  ['gr', '57,27', '+5,15+8,99%', '892.110', '+52.969+5,94%'],
  ['1 Tahun', 'Kurs', '', '', '14.526', '+614+4,23%'],
  ['oz', '1.851,10', '+90,46+4,89%', '26.889.079', '+2.506.140+9,32%'],
  ['gr', '59,51', '+2,91+4,89%', '864.504', '+80.574+9,32%'],
  ['2 Tahun', 'Kurs', '', '', '14.297', '+843+5,90%'],
  ['oz', '1.891,24', '+50,32+2,66%', '27.039.077', '+2.356.141+8,71%'],
  ['gr', '60,80', '+1,62+2,66%', '869.327', '+75.752+8,71%'],
  ['3 Tahun', 'Kurs', '', '', '14.100', '+1.040+7,38%'],
  ['oz', '1.682,73', '+258,83+15,38%', '23.726.493', '+5.668.725+23,89%'],
  ['gr', '54,10', '+8,32+15,38%', '762.824', '+182.254+23,89%'],
  ['5 Tahun', 'Kurs', '', '', '13.875', '+1.265+9,12%'],
  ['oz', '1.299,44', '+642,12+49,42%', '18.029.730', '+11.365.488+63,04%'],
  ['gr', '41,78', '+20,64+49,42%', '579.669', '+365.409+63,04%']])
(['Home', 'Emas 1 Gram', 'History', 'Trend', 'Perak 1 Gram'],
 [[''],
  ['Emas 24 KaratHarga Emas 1 Gram', ''],
  ['USD', '62,42↓', '-0,22-0,35%'],
  ['KURS', '14.869,85↓', '-32,05-0,22%'],
  ['IDR', '928.214,75↓', '-5.181,92-0,56%'],
  ['Senin, 05 Juni 2023 19:12']],
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
  ['USD', '62,64', '62,42 - 62,64', '62,53'],
  ['KURS', '14.901,90', '14.869,85 - 14.901,90', '14.885,88'],
  ['IDR', '933.396,67', '928.214,75 - 933.396,67', '930.805,71'],
  [''],
  ['', 'Awal Tahun', 'Pergerakkan YTD', '+/- YTD'],
  ['USD', '58,64', '58,23 - 65,97', '+3,78 (6,45%)'],
  ['KURS', '15.538,50', '14.669,40 - 15.629,15', '-668,65(-4,30%)'],
  ['IDR', '911.153,72', '888.842,84 - 982.694,10', '+17.061,03 (1,87%)'],
  [''],
  ['', 'Tahun Lalu / 52 Minggu', 'Pergerakkan 52 Minggu', '+/- 52 Minggu'],
  ['USD', '59,51', '52,31 - 65,97', '+2,91 (4,89%)'],
  ['KURS', '14.433,50', '14.431,75 - 15.785,40', '+436,35 (3,02%)'],
  ['IDR', '858.998,88', '795.009,21 - 982.694,10', '+69.215,87 (8,06%)']])
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
{'a': <generator object ExampleComparePerformance.a.<locals>.<genexpr> at 0x0000014075FD2B30>,
 'b': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
 'c': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 'd': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
{'a': 100, 'b': 144, 'c': 117, 'd': 157}
{'a': 100, 'b': 146, 'c': 115, 'd': 166}
{'a': 100, 'b': 134, 'c': 124, 'd': 156}
{'a': 100, 'b': 140, 'c': 112, 'd': 151}
{'a': 100, 'b': 114, 'c': 115, 'd': 117}
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

## html_dl

`html_dl`

Class ini digunakan untuk serialize dan unserialize html

## html_ol

`html_ol`

Class ini digunakan untuk serialize dan unserialize html

## html_table

`html_table`

Class ini digunakan untuk serialize dan unserialize html

## html_ul

`html_ul`

Class ini digunakan untuk serialize dan unserialize html
