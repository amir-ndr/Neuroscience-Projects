import torch
from pymonntorch import Behavior, SynapseGroup, Network, NeuronGroup, Recorder, EventRecorder
import matplotlib.pyplot as plt
from matplotlib.pyplot import  Button, Slider

class Izhikevich(Behavior):
    
    def initialize(self, neurons):
        super().initialize(neurons)
        self.add_tag("Izhikevich")
        self.set_parameters_as_variables(neurons)
        neurons.a *= neurons.vector('ones')
        neurons.b *= neurons.vector('ones')
        neurons.c *= neurons.vector('ones')
        neurons.d *= neurons.vector('ones')
        neurons.v = neurons.vector(mode="ones") * neurons.v_rest
        neurons.I = neurons.vector(mode="zeros")
        neurons.spikes = neurons.vector(mode="zeros")
        neurons.membrane_recovery = neurons.vector(mode="ones") * neurons.u
        
    def _dv_dt(self, neurons):
        res = neurons.dt * (0.04 * neurons.v**2 + 5*neurons.v + 140 - neurons.membrane_recovery + neurons.I)
        return res
    
    def _du_dt(self, neurons):
        return neurons.dt * (neurons.a * (neurons.b * neurons.v - neurons.membrane_recovery))
    
    def _fire(self, neurons):
        neurons.v[neurons.spikes] = neurons.c[neurons.spikes]
        neurons.membrane_recovery[neurons.spikes] += neurons.d[neurons.spikes]
        
    def forward(self, neurons):
        neurons.spikes = neurons.v >= 30.
        if torch.sum(neurons.spikes) > 0:
            self._fire(neurons)
        neurons.v += self._dv_dt(neurons) #* neurons.dt
        neurons.membrane_recovery += self._du_dt(neurons) #* neurons.dt

class Izhikevich_input(Behavior):              

    def initialize(self, neurons):
        super().initialize(neurons)
        for synapse in neurons.afferent_synapses['All']:
            synapse.W = synapse.matrix(mode='uniform')
            synapse.enabled = synapse.W > 0
    
    def _get_spikes(self, synapse):
        spikes = synapse.src.spikes.float()
        return torch.matmul(synapse.W, spikes)

    def forward(self, neurons):
        neurons.I = neurons.E_I[neurons.iteration-1]
        for synapse in neurons.afferent_synapses['GLUTAMATE']: 
            neurons.I += 0.5*(self._get_spikes(synapse) / synapse.src.size )


def stream_izh(mode = 'step', I_init=10., a=0.02, b=0.2, c=-50., d=8., mean_=10., std_=2., iter=1000):

    ITER = iter
    EXC_SIZE = 1
    I_EXC_NOISE_ = torch.normal(mean=mean_, std=std_, size=(ITER,EXC_SIZE))
    I_EXC_STEP_ = torch.zeros(size=(ITER,EXC_SIZE))
    I_EXC_STEP_[150:750,:] = I_init
    I_out = I_EXC_STEP_ if mode == 'step' else I_EXC_NOISE_
    EXC_CONFIG = {"c" : c,
        "E_I" : I_out,
        "a": a,
        "b": b,
        "d": d,
        "dt": 0.5,
        "u": -8.,
        "v_rest": -65.,
        }
    my_net = Network()
    ng_exc = NeuronGroup(
        net=my_net,
        size=EXC_SIZE,
        tag="exc_neurons",
        behavior={
            1: Izhikevich(**EXC_CONFIG),
            2: Izhikevich_input(),
            9: Recorder(["n.v", "torch.mean(n.v)", "n.I", "n.membrane_recovery"], auto_annotate=False),
            10: EventRecorder(["spikes"]),
        },
    )

    SynapseGroup(src=ng_exc, dst=ng_exc, net=my_net, tag="GLUTAMATE")

    my_net.initialize()
    my_net.simulate_iterations(ITER)
    
    return my_net["n.v",0][:, :1], I_out


def interactive_izh(mode = 'step', iter_init=1000):  

    I_init = 10.
    a_init = 0.02
    b_init = 0.2
    c_init = -65.
    d_init = 8.
    mean_init = 20.
    std_init = 3.

    axis_color = 'lightgoldenrodyellow'

    fig = plt.figure("Izhikevich Neuron", figsize=(16, 10))
    ax = fig.add_subplot(111)
    plt.title("Interactive Izhikevich Neuron")
    fig.subplots_adjust(left=0.1, bottom=0.5)
    # print(net["n.v",0][:, :1].shape)
    line = plt.plot(torch.ones((iter_init))*1., label="Membrane Potential")[0]
    line2 = plt.plot(torch.ones((iter_init))*1., label="Applied Current")[0]
    line3 = plt.plot(torch.ones((iter_init))* 30., label="Threshold Voltage")
    plt.ylim([-100, 220])

    plt.legend(loc="upper right")

    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")

    if mode == "step":


        I_slider_axis = plt.axes([0.1, 0.40, 0.65, 0.03], facecolor=axis_color)
        I_slider = Slider(I_slider_axis, '$I_{ext}$ ', 0.1, 40, valinit=I_init, valfmt='%i')

        a_slider_axis = plt.axes([0.1, 0.35, 0.65, 0.03], facecolor=axis_color)
        a_slider = Slider(a_slider_axis, '$a$', 0.001, 0.15, valinit=a_init)

        b_slider_axis = plt.axes([0.1, 0.30, 0.65, 0.03], facecolor=axis_color)
        b_slider = Slider(b_slider_axis, '$b$', 0.001, 0.3, valinit=b_init)

        c_slider_axis = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axis_color)
        c_slider = Slider(c_slider_axis, '$c$', -75, -40, valinit=c_init)

        d_slider_axis = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor=axis_color)
        d_slider = Slider(d_slider_axis, '$d$', 0.001, 10, valinit=d_init)

        def update(val):
            v, i = stream_izh(mode=mode, I_init=I_slider.val, a=a_slider.val, b=b_slider.val, c=c_slider.val, d=d_slider.val,
            mean_=mean_init, std_=std_init, iter=iter_init)
            line.set_ydata(v)
            line2.set_ydata(i)

        I_slider.on_changed(update)
        a_slider.on_changed(update)
        b_slider.on_changed(update)
        c_slider.on_changed(update)
        d_slider.on_changed(update)

        RS_button_ax = plt.axes([0.1, 0.1, 0.15, 0.04])
        RS_button = Button(RS_button_ax, 'REGULAR SPIKING', color=axis_color, hovercolor='0.975')

        def RS_button_was_clicked(event):
            a_slider.reset()
            b_slider.reset()
            c_slider.reset()
            d_slider.reset()

        RS_button.on_clicked(RS_button_was_clicked)

        IB_button_ax = plt.axes([0.35, 0.1, 0.15, 0.04])
        IB_button = Button(
            IB_button_ax,
            'INTRINSICALLY BURSTING',
            color=axis_color,
            hovercolor='0.975')

        def IB_button_was_clicked(event):
            a_slider.reset()
            b_slider.reset()
            c_slider.set_val(-55)
            d_slider.set_val(4)

        IB_button.on_clicked(IB_button_was_clicked)

        CH_button_ax = plt.axes([0.6, 0.1, 0.15, 0.04])
        CH_button = Button(CH_button_ax, 'CHATTERING', color=axis_color, hovercolor='0.975')

        def CH_button_was_clicked(event):
            a_slider.reset()
            b_slider.reset()
            c_slider.set_val(-50)
            d_slider.set_val(2)

        CH_button.on_clicked(CH_button_was_clicked)

        FS_button_ax = plt.axes([0.1, 0.02, 0.15, 0.04])
        FS_button = Button(
            FS_button_ax, 'FAST SPIKING', color=axis_color, hovercolor='0.975')

        def FS_button_was_clicked(event):
            a_slider.set_val(0.1)
            b_slider.reset()
            c_slider.reset()
            d_slider.reset()

        FS_button.on_clicked(FS_button_was_clicked)

        LTS_button_ax = plt.axes([0.35, 0.02, 0.15, 0.04])
        LTS_button = Button(
            LTS_button_ax,
            'LOW-THRESHOLD SPIKING',
            color=axis_color,
            hovercolor='0.975')

        def LTS_button_was_clicked(event):
            a_slider.reset()
            b_slider.set_val(0.25)
            c_slider.reset()
            d_slider.reset()

        LTS_button.on_clicked(LTS_button_was_clicked)

        RZ_button_ax = plt.axes([0.6, 0.02, 0.15, 0.04])
        RZ_button_ = Button(
            RZ_button_ax, 'RESONATOR', color=axis_color, hovercolor='0.975')

        def RZ_button_was_clicked(event):
            a_slider.set_val(0.1)
            b_slider.set_val(0.26)
            c_slider.reset()
            d_slider.reset()

        RZ_button_.on_clicked(RZ_button_was_clicked)

    elif mode == 'noise':

        a_slider_axis = plt.axes([0.1, 0.40, 0.65, 0.03], facecolor=axis_color)
        a_slider = Slider(a_slider_axis, '$a$', 0.001, 0.15, valinit=a_init)

        b_slider_axis = plt.axes([0.1, 0.35, 0.65, 0.03], facecolor=axis_color)
        b_slider = Slider(b_slider_axis, '$b$', 0.001, 0.3, valinit=b_init)

        c_slider_axis = plt.axes([0.1, 0.30, 0.65, 0.03], facecolor=axis_color)
        c_slider = Slider(c_slider_axis, '$c$', -75, -40, valinit=c_init)

        d_slider_axis = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axis_color)
        d_slider = Slider(d_slider_axis, '$d$', 0.001, 10, valinit=d_init)

        def update(val):
            v, i = stream_izh(mode=mode, I_init=10., a=a_slider.val, b=b_slider.val, c=c_slider.val, d=d_slider.val,
            mean_=mean_slider.val, std_=std_slider.val, iter=iter_init)
            line.set_ydata(v)
            line2.set_ydata(i)

        mean_slider_axis = plt.axes([0.1, 0.20, 0.65, 0.03], facecolor=axis_color)
        mean_slider = Slider(mean_slider_axis, '$I-mean(noisy)$', 1., 200., valinit=mean_init)

        std_slider_axis = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axis_color)
        std_slider = Slider(std_slider_axis, '$I-std(noisy)$', 1., 40., valinit=std_init)
        # I_slider.on_changed(update)
        a_slider.on_changed(update)
        b_slider.on_changed(update)
        c_slider.on_changed(update)
        d_slider.on_changed(update)
        mean_slider.on_changed(update)
        std_slider.on_changed(update)

    plt.show()

mode = str(input('choose your mode: (step OR noise)'))
iterations = 1000
interactive_izh(mode, iterations)