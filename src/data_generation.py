import numpy as np
def generate_sar(seed=11,h=100,w=100):
    rng=np.random.default_rng(seed); xx,yy=np.meshgrid(np.linspace(-1,1,w),np.linspace(-1,1,h)); river=np.abs(xx)<.10
    truth=((xx+.2)**2+(yy-.1)**2<.35**2)|river; pre=-10+rng.normal(0,1.5,(h,w)); post=pre.copy(); post[truth]-=6+rng.normal(0,.7,truth.sum()); return pre,post,truth
