import time

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class TimeItMiddleware(MiddlewareMixin):
	def process_request(self, request):
		self.start_time = time.time()
		return
		'''
		这是请求来到middleware 中时进入的第一个方法。一般情况下，我们可以在这里做一些校验，比如用户登录或者HTTP 中是否有认证头之类的验证。这个方法可以有两种返回值——HttpResponse或者None。如返回HttpResponse，那么接下来的处理方式只会执行process_response, 其他方法将不会被执行。
		这里需要注意的是，如果你的middleware 是settings配置的MIDDLEWARE 的第一个，那么剩下的middleware 也不会执行；如果返回None，那么Django会继续执行其他方法
		'''
	
	def process_view(self, request, func, *arg, **kwargs):
		if request.path != reverse('index'):
			return None
		
		start = time.time()
		response = func(request)
		costed = time.time() - start
		print('process view: {:.2f}s',format(costed))
		return response
		'''
		这个方法是在process_request 方法之后执行的，参数如上面代码所示，其中func 就是我们将要执行的view方法。因此如果要统计一个view 的执行时间，可以在这里做。
		它的返回值跟process_request 一样，是HttpResponse或None，其逻辑也一样。如果返回None，那么Django会帮你执行view函数，从而得到最终的response
		'''
		
	def process_exception(self, request, exception):
		costed = time.time() - self.start_time
		print('request to response cose: {:2f}s'.format(costed)
		return response
		'''
		其他的处理方法是按顺序介绍的，而这个方法不太一样。只要在发生异常时，才会进入这个方法。
		哪个阶段发生的异常呢？可以简单理解为在将要调用的View中出现一次（就是在process_view的func函数中）或者返回的模板response在渲染时发生的一次。但是需要注意的是，如果你在process_view中手动调用了func，就不会触发process_exception了。这个方法接收到异常之后，可以选择处理异常，然后返回一个含有异常信息的HttpResponse，或者直接返回None不处理，这种情况下Django 会使用自己的异常模板
		'''
		
	def process_template_response(self, request, response):
		return response
		'''
		执行完上面的方法，并且Django帮我们执行完view，拿到最终的response 后，如果使用了模板的response （这是通过return render(request, 'index.html', context={})方式返回的response),就会来到这个方法中。
		在这个方法中，我们可以对response 做一下操作，比如Content-Type 设置，或者其他header的修改/增加
		'''
		
	def process_response(self, request, response):
		return response
		'''
		当所有流程都处理完毕后，就来到了这个方法。
		这个方法的逻辑跟process_template_response 是完全一样的，只是后者是针对带有模板的response的处理
		'''
