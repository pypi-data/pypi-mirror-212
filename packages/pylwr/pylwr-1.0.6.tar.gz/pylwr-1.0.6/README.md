# Python第三方包二次封装

应该会用到一些其他依赖

## 安装

```shell
pip install pylwr
```

打包与上传

```shell
py -m build
python setup.py sdist bdist_wheel
py -m twine upload dist\*
```
