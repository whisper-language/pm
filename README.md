# pm 软件包管理器
package manager


project->local->global

## 查看wpm 帮助文件
```
wpm help
```

```
wpm  command <options>
	init 							初始化一个项目
	clean							删除所有依赖
	package							打包到一个压缩文件
	update  						更新项目依赖
	search <package_name>  					搜索指定依赖包
	install <package_name>  				安装指定依赖包
	uninstall <package_name> 				卸载指定依赖包
	tidy							清理无用的依赖
	run 							运行指定 wpn 脚本
	config get k 						获取指定配置
	config set k v		 				修改指定配置
	help							打印帮助信息
	version							打印版本信息
```

## 创建 whisper 项目
```
wpm --init <package_name>
```

## 更新 wpm 项目
```
wpm --update
```

## 在 global 仓库内搜索 whisper扩展
```
wpm --search <package_name>
```

## 安装 wpm 扩展包
```
wpm --install <package_name>  -g
```

## 执行 wpm 命令
```
wpm --uninstall <package_name>  -g
```

## 清理 wpm 命令 删除无用的 依赖包
```
wpm --tidy
```

## 执行 wpm 命令
```
wpm --run  <name>
```

## 获取wpm配置
```
wpm --config get k
```

## 设置wpm配置
```
wpm --config set k=v
```
