import numpy as np

""" Input variables """
S = 30.0 # m^2 (Surface area wing)
c = 2.0569 # m (MAC)
b = 15.911 # m (Wing span)
e = 0.8 # (Oswald efficiency factor)
mu_c = 5
mu_b = 5
D_c = 5
D_b = 5
C_D0 = 0.04 # (Zero drag coefficient)
C_La = 5.084 # (dC_L/da)
Ks_xx = 0.019 # (Radius of gyration about x)
Ks_yy = 1.3925 # (Radius of gyration about y)
Ks_zz = 0.042 # (Radius of gyration about z)
Ks_xy = 0.002 # (Product of inertia)
ks_xz = 0.002

""" Linear model stability derivatives - symmetric flight """
# Longitudinal force derivatives
C_X0 = -0.5
C_Xu = -0.0279 # (dC_X / du)
C_Xa = -0.4797 # (dC_X / dalpha)
C_Xda = 0.0833 # (dC_X / dalpha_dot)
C_Xq = -0.2817 # (dC_X / dq)
C_Xdelta = -0.0373 # (dC_X / ddelta)
C_Xdeltae = -0.5

# Normal force derivatives
C_Z0 = -0.5
C_Zu = -0.3762 # (dC_Z / du)
C_Za = -5.7434 # (dC_Z / dalpha)
C_Zda = -0.0035 # (dC_Z / dalpha_dot)
C_Zq = -5.6629 # (dC_Z / dq)
C_Zdelta = -0.6961 # (dC_Z / ddelta)
C_Zdeltae = -0.5

#Pitch moment derivatives
C_m0 = 0.0297 # (C_m0)
C_mu = 0.0699 # (dC_m / du)
C_ma = -0.5626 # (dC_m / dalpha)
C_mda = 0.1780 # (dC_m / dalpha_dot)
C_mq = -8.7941 # (dC_m / dq)
C_mdelta = -1.1642 # (dC_m / ddelta)
C_mTc = -0.0064 # (dC_m / dTc)
C_mdeltae = -0.5

""" Linear model stability derivatives - asymmetric flight """
# Lateral force derivatives
C_Yb = -0.7500 # (dC_Y / dbeta)
C_Ydb = 0 # (dC_Y / dbeta_dot)
C_Yp = -0.0304 # (dC_Y / dp)
C_Yr = 0.8495 # (dC_Y / dr)
C_Ydeltaa = -0.0400 # (dC_Y / delta_a)
C_Ydeltar = 0.2300 # (dC_Y / delta_r)

# Roll moment derivatives
C_L = 0.35
C_lb = -0.1026 # (dC_l / dbeta)
C_lp = -0.7108 # (dC_l / dp)
C_lr = 0.2376 # (dC_l / dr)
C_ldeltaa = -0.2309 # (dC_l / delta_a)
C_ldeltar = 0.0344 # (dC_l / delta_r)

# Yaw moment derivatives
C_nb = 0.1348 # (dC_n / dbeta)
C_ndb = 0 # (dC_n / dbeta_dot)
C_np = -0.0602 # (dC_n / dp)
C_nr = -0.2061 # (dC_n / dr)
C_ndeltaa = -0.0120 # (dC_n / delta_a)
C_ndeltar = -0.0939 # (dC_n / delta_r)

""" Variables not sure needed """
W_s = 60500 # N (standard aircraft mass)
m_fs = 0.048 # kg/s (standard engine fuel flow per engine)
rho_0 = 1.225 # kg/m^3 (standard air density)

""" Total mass computation """
M_r = 6000 # inch or kg (ramp mass)

""" Equations of symmetric motion """
Asym = np.array([[C_Xu-2*mu_c*D_c, C_Xa, C_Z0, 0],
                 [C_Zu, C_Za+(C_Zda-2*mu_c)*D_c, -C_X0, C_Zq+2*mu_c],
                 [0, 0, -D_c, 1],
                 [C_mu, C_ma+C_mda*D_c, 0, C_mq-2*mu_c*Ks_yy*D_c]])
Bsym = np.array([-C_Xdeltae, -C_Zdeltae, 0, -C_mdeltae])

Aasym = np.array([[C_Yb+(C_Ydb-2*mu_b)*D_b, C_L, C_Yp, C_Yr-4*mu_b],
                  [0, -0.5*D_b, 1, 0],
                  [C_lb, 0, C_lp-4*mu_b*ks_xx*D_b, C_lr+4*mu_b*ks_xz*D_b],
                  [C_nb+C_ndb*D_b, 0, C_np+4*mu_b*ks_xz*D_b, C_nr-4*mu_b*ks_zz*D_b])
Basym = np.array([[-C_Ydeltaa, -C_Ydeltar],
                 [0,0],
                 [-C_ldeltaa, -C_ldeltar],
                 [-C_ndeltaa, -C_ndeltar]])
