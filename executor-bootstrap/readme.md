## executor-bootstrap

The bootstrap c/c++ project of design bootcamp.

- setup

```sh
$ git clone git@github.com:joycode-bootcamp/executor-bootstrap.git
$ cd executor-bootstrap
$ chmod a+x ./ccup.sh
```

- build&test

Make sure that docker is pre installed on the system.

```sh
$ cd executor-bootstrap

# launch docker environment, wait until the image download completely.
./ccup.sh -e

# update the dependent codes
$ ./ccup.sh -u

# build
$ ./ccup.sh -b

# test
$ ./ccup.sh -t
```

- usage

```sh
# start project from docker env
./ccup.sh -e

# update depends
./ccup.sh -u

# build
./ccup.sh -b

# update & build
./ccup.sh -ub

# run tests
./ccup.sh -t

# build & test
./ccup.sh -bt

# update & build & test
./ccup.sh -ubt

# run executable
./ccup.sh -r

# install
./ccup.sh -i

# build & install
./ccup.sh -bi

# update & build & install
./ccup.sh -ubi

# clean build
./ccup.sh -c

# clean all
./ccup.sh -C

# help
./ccup.sh -h
```


```markdown
代码风格要求：类成员变量要求 m_开头的小驼峰形式，类成员函数用大驼峰形式，函数大括号需要换行，函数中的条件等大括号不需要换行；
代码需要符合开闭原则，要求可扩展性，也要求最小设计原则

pre1
Executor组件对Config组件提供初始化接口，负责将扫地机初始化在指定位置(x,y,heading)；其中x,y为整数类型；heading对应四个方向（东南西北）
Executor组件可以执行Controller组件发来的如下动作指令
- turn right:右转90度，位置不变；
- turn left：右转90度，位置不变；
- Controller组件可以从Executor 组件获取扫地机当前的坐标位置和朝向；如果Executor组件未被初始化位置，则接口默认返回0，以及朝向北

- 要求：自行设计Executor组件对外的接口，实现上述功能，需要有测试用例

pre2
- Executor 组件可以执行Controller 组件发来的如下动作指令：
 * forward: 沿当前朝向前进一步，方向不变
 * backward： 沿当前朝向后进一步，方向不变
注意：x轴移动的方向为东西方向，y轴移动的方向为南北方向
```