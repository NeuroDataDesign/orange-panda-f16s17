clear
close all

%% setting up data
Fs = 1000;            % Sampling frequency
T = 2/Fs;             % Sampling period
L = 1000;             % Length of signal
t = (0:L-1)*T;        % Time vector
w = 10*pi;

% S = 0.8*sin(w*t) + 0.6*sin(w*sin(w*t));
S = 0.8*sin(w*t) + 0.4*sin(0.5*w*t);

figure(1)
subplot(121)
plot(1000*t, S)
xlabel('t (milliseconds)')
ylabel('X(t)')

subplot(122)
Y = fftshift(abs(fft(S)/L));
f = Fs*((-L/2):(L-1)/2)/L;
plot(f,Y)
xlabel('f (Hz)')
ylabel('|P1(f)|')

%% adding noise
X = S + sin(60*pi*t) + 2*randn(size(t));  

figure(2)
subplot(121)
plot(1000*t, X)
xlabel('t (milliseconds)')
ylabel('X(t)')

subplot(122)
Y_ns = fftshift(abs(fft(X)/L));
f = Fs*((-L/2):(L-1)/2)/L;
plot(f,Y_ns)
xlabel('f (Hz)')
ylabel('|P1(f)|')


%% lowpass butterworth at 300 Hz
fc = 40;
Fs = 1000;

[b,a] = butter(6,fc/(Fs/2));
% freqz(b,a)

X_lp = filter(b, a, X);

figure(3)
subplot(121)
plot(1000*t, X_lp)
xlabel('t (milliseconds)')
ylabel('X_lp(t)')

subplot(122)
Y_lp = fftshift(abs(fft(X_lp)/L));
f = Fs*((-L/2):(L-1)/2)/L;
plot(f,Y_lp)
xlabel('f (Hz)')
ylabel('|P1(f)|')

%% bandstop butterworth with edges at 0.2 pi and 0.6 pi
[b,a] = butter(3,[0.21 0.8],'stop');
% freqz(b,a)

X_bs = filter(b, a, X);

figure(4)
subplot(121)
plot(1000*t, X_bs)
xlabel('t (milliseconds)')
ylabel('X_lp(t)')

subplot(122)
Y_bs = fftshift(abs(fft(X_bs)/L));
f = Fs*((-L/2):(L-1)/2)/L;
plot(f,Y_bs)
xlabel('f (Hz)')
ylabel('|P1(f)|')
