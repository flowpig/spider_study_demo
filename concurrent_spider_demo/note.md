        ```
        Python中的Futures模块，位于concurrent.futures和asyncio中，它们都表示带有延迟的操作。Futures会将处于等待状态的操作包裹起来放到队列中，这些操作的状态随时可以查询，当然，它们的结果或是异常，也能够在操作完成后被获取。
	
	通常来说，作为用户，我们不用考虑如何去创建Futures，这些Futures底层都会帮我们处理好。我们要做的，实际上是去schedule这些Futures的执行。
	
	比如，Futures中的Executor类，当我们执行executor.submit(func)时，它便会安排里面的func()函数执行，并返回创建好的future实例，以便之后查询调用。
	
	Futures中的方法done()，表示相对应的操作是否完成,True表示完成，False表示没有完成。不过，要注意，done()是non-blocking的，会立即返回结果。相对应的add_done_calback(fn), 则表示Futures完成后，相对应的参数函数fn,会被通知并执行调用。
	
	Futures中还有一个重要的函数result()，它表示当future完成后，返回其对应的结果或异常。而as_completed(fs)，则是针对给定的future迭代器fs，在其完成后，返回完成后的迭代器。
	
	所以multi_thread_spider.py也可以写成multi_thread_spider01.py
	```


