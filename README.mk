##About the WeDo


The [Lego WeDo](http://education.lego.com/en-us/lego-education-product-database/wedo/9580-lego-education-wedo-construction-set/) is a tethered-over-USB sensing and robotics toolkit produced by Lego for the educational market. 


It's gotten lots of press, including a favorable review on the One Laptop Per Child blog, on [deployments and training in Peru.](http://blog.laptop.org/2011/02/12/lego-wedo-oloc-peru/)

It's supported by Scratch(on Windows and OSX) and by Lego's proprietary software(on Windows.)

It prominently features the [LB1836](http://semicon.sanyo.com/en/ds_e/EN3947F.pdf) motor driver and the [LM358](http://www.national.com/ds/LM/LM158.pdf) op-amp, as well as an epoxy blob with USB support.

The digital communication protocol used by the Power Functions system is documented on [Philo's Awesome Page](http://www.philohome.com/pf/LEGO_Power_Functions_RC.pdf).

##How to Use it

```python
>>> from wedo import WeDo
>>> wd = WeDo()
>>> wd.setMotorB(100)  # forward motor B full speed
>>> wd.setMotorB(0)    # stop motor B
>>> wd.setMotorB(-50)  # reverse motor B half speed
```

