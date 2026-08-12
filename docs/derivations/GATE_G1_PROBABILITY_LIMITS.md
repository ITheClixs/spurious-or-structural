# G1 probability limits

## Claim being derived

For the simultaneous system

$$
r_t = \Lambda q_t + \Gamma f_t + u_t,
\qquad
q_t = B r_t + \Delta_f f_t + v_t,
$$

ordinary least squares does not generally recover the structural cross-impact
matrix $\Lambda$. The population coefficient contains separate latent-factor
and simultaneity terms. Controlling for $\widehat f_t=f_t+\epsilon_t$ replaces
the factor covariance in the first term by the factor variance left after
linear projection on the noisy proxy; it does not remove simultaneity.

## Dimensions, conventions, and assumptions

- $r_t,q_t,u_t,v_t\in\mathbb R^N$ and
  $f_t,\epsilon_t\in\mathbb R^K$.
- $\Lambda,B\in\mathbb R^{N\times N}$ and
  $\Gamma,\Delta_f\in\mathbb R^{N\times K}$.
- All variables are centered. An intercept therefore changes none of the
  formulas below.
- $f_t,u_t,v_t,\epsilon_t$ are mutually uncorrelated at time $t$, with
  covariance matrices $\Sigma_f,\Sigma_u,\Sigma_v,\Sigma_\epsilon$.
  Independence is sufficient but stronger than required.
- The observations obey a law of large numbers and have finite second moments.
  IID sampling is not needed for the probability limits, although dependence
  changes the inference method.
- $I_N-B\Lambda$, the relevant regressor covariance, and the proxy covariance
  are nonsingular. A singular covariance would define a pseudoinverse-dependent
  estimand rather than a unique OLS coefficient.

The requested primitive-only expressions are impossible without the stated
zero cross-covariances. If, for example, $\operatorname{Cov}(u,v)\ne0$, its
value enters both the reduced-form flow covariance and the bias.

For column-vector structural notation, define the population regression matrix
$A$ by

$$
A=\arg\min_C \operatorname E\|r_t-Cq_t\|_2^2.
$$

Then $A=\Sigma_{rq}\Sigma_{qq}^{-1}$. With row-stacked software matrices,
the usual output $(Q^\top Q)^{-1}Q^\top R$ estimates $A^\top$; this
transpose is an explicit implementation invariant for the G1 verifier.

## 1. Simultaneous reduced form

Substitute the return equation into the flow equation:

$$
\begin{aligned}
q_t
&=B(\Lambda q_t+\Gamma f_t+u_t)+\Delta_f f_t+v_t,\\
(I_N-B\Lambda)q_t
&=(B\Gamma+\Delta_f)f_t+Bu_t+v_t.
\end{aligned}
$$

Write

$$
L=I_N-B\Lambda,
\qquad H=L^{-1},
\qquad D=B\Gamma+\Delta_f.
$$

The flow reduced form is

$$
\boxed{q_t=HDf_t+HBu_t+Hv_t.}
$$

It is convenient to set $P=HD$, $U=HB$, and $V=H$. Mutual
uncorrelatedness gives

$$
\Sigma_{qq}
=P\Sigma_fP^\top+U\Sigma_uU^\top+V\Sigma_vV^\top,
$$

$$
\operatorname{Cov}(f_t,q_t)=\Sigma_fP^\top,
\qquad
\operatorname{Cov}(u_t,q_t)=\Sigma_uU^\top.
$$

Only nonsingularity of $L$ is required for this algebra. The stronger
condition $\rho(B\Lambda)<1$ is an economic feedback-stability condition,
not a hidden mathematical requirement; the precommitted simulation will impose
it as a numerical safety margin.

## 2. OLS without the factor

Using the structural return equation,

$$
\begin{aligned}
\Sigma_{rq}
&=\operatorname{Cov}(\Lambda q_t+\Gamma f_t+u_t,q_t)\\
&=\Lambda\Sigma_{qq}+\Gamma\Sigma_fP^\top+\Sigma_uU^\top.
\end{aligned}
$$

Therefore

$$
\boxed{
\operatorname{plim}\widehat\Lambda_{\mathrm{OLS}}
=\Lambda
+\underbrace{\Gamma\Sigma_fP^\top\Sigma_{qq}^{-1}}_{
  \text{latent-factor confounding}}
+\underbrace{\Sigma_uU^\top\Sigma_{qq}^{-1}}_{
  \text{within-bin simultaneity}}.
}
$$

This is already in structural parameters because
$P=(I_N-B\Lambda)^{-1}(B\Gamma+\Delta_f)$ and
$U=(I_N-B\Lambda)^{-1}B$. An equivalent fully expanded form makes the
primitive dependence especially clear. Let

$$
\Omega_q=D\Sigma_fD^\top+B\Sigma_uB^\top+\Sigma_v.
$$

Since $\Sigma_{qq}=H\Omega_qH^\top$, cancellation of $H^\top$ yields

$$
\boxed{
\operatorname{plim}\widehat\Lambda_{\mathrm{OLS}}
=\Lambda+
(\Gamma\Sigma_fD^\top+\Sigma_uB^\top)
\Omega_q^{-1}(I_N-B\Lambda).
}
$$

The two summands inside the first parentheses are, respectively, the
confounding and simultaneity numerators. Either can be non-diagonal even when
the structural $\Lambda$ is diagonal.

## 3. OLS with a noisy factor proxy

Let

$$
h_t=\widehat f_t=f_t+\epsilon_t,
\qquad
S_h=\operatorname{Var}(h_t)=\Sigma_f+\Sigma_\epsilon.
$$

The linear-projection residual of the true factor after controlling for $h_t$
is

$$
f_t^\perp=f_t-\Sigma_fS_h^{-1}h_t,
$$

with covariance

$$
\boxed{
R_f
=\operatorname{Var}(f_t^\perp)
=\Sigma_f-\Sigma_f(\Sigma_f+\Sigma_\epsilon)^{-1}\Sigma_f.
}
$$

When $\Sigma_f$ and $\Sigma_\epsilon$ are positive definite, the same
matrix is
$(\Sigma_f^{-1}+\Sigma_\epsilon^{-1})^{-1}$. Matrix order matters; in
general there is no scalar reliability ratio.

Frisch--Waugh--Lovell residualization gives

$$
q_t^\perp
=q_t-\operatorname{Cov}(q_t,h_t)S_h^{-1}h_t
=P f_t^\perp+Uu_t+Vv_t
$$

and hence

$$
Q_h
=\operatorname{Var}(q_t^\perp)
=P R_fP^\top+U\Sigma_uU^\top+V\Sigma_vV^\top.
$$

Residualizing the return equation by the same projection gives

$$
r_t^\perp=\Lambda q_t^\perp+\Gamma f_t^\perp+u_t.
$$

The population coefficient on $q_t$ in the regression of $r_t$ on
$[q_t,h_t]$ is therefore

$$
\boxed{
\operatorname{plim}\widehat\Lambda_{q\mid h}
=\Lambda
+\underbrace{\Gamma R_fP^\top Q_h^{-1}}_{
  \text{unabsorbed factor confounding}}
+\underbrace{\Sigma_uU^\top Q_h^{-1}}_{
  \text{within-bin simultaneity}}.
}
$$

Define

$$
\Omega_{q\mid h}
=D R_fD^\top+B\Sigma_uB^\top+\Sigma_v.
$$

Because $Q_h=H\Omega_{q\mid h}H^\top$, the primitive-only version is

$$
\boxed{
\operatorname{plim}\widehat\Lambda_{q\mid h}
=\Lambda+
(\Gamma R_fD^\top+\Sigma_uB^\top)
\Omega_{q\mid h}^{-1}(I_N-B\Lambda).
}
$$

## 4. Predictions that must survive simulation

These are algebraic directional predictions, not fitted observations.

1. **Perfect proxy:** if $\Sigma_\epsilon=0$, then $R_f=0$. Factor
   confounding disappears exactly, but the simultaneity term remains unless its
   numerator is zero.
2. **Useless proxy:** if
   $\Sigma_\epsilon=c\Omega$ with $\Omega\succ0$ and $c\to\infty$, then
   $R_f\to\Sigma_f$, $Q_h\to\Sigma_{qq}$, and controlled OLS converges to
   uncontrolled OLS.
3. **No feedback:** if $B=0$, then $H=V=I_N$, $U=0$, and

   $$
   \operatorname{plim}\widehat\Lambda_{q\mid h}
   =\Lambda+\Gamma R_f\Delta_f^\top
   (\Delta_fR_f\Delta_f^\top+\Sigma_v)^{-1}.
   $$

   A perfect proxy is then sufficient for recovery of $\Lambda$.
4. **No direct factor-to-flow loading is not enough:** if $\Delta_f=0$, the
   factor still reaches flow through $B\Gamma$, so confounding can remain.
5. **Zero structural impact need not imply zero regression impact:** setting
   $\Lambda=0$ leaves both bias terms available to create off-diagonal
   population coefficients.
6. **Scalar factor-free cross-check:** for
   $r=\lambda q+u$, $q=br+v$,

   $$
   \operatorname{plim}\widehat\lambda
   =\frac{\lambda\sigma_v^2+b\sigma_u^2}
          {b^2\sigma_u^2+\sigma_v^2}.
   $$

A more accurate proxy lowers $R_f$ in positive-semidefinite order. It does
**not** follow that every element of the total coefficient bias shrinks
monotonically: $Q_h^{-1}$ changes at the same time and reweights both bias
components. The simulation prediction must test the exact matrix formula, not
a scalar attenuation slogan.

## 5. What this derivation does not claim

- It does not identify $\Lambda$; it derives the pseudo-true coefficients of
  two regressions.
- It does not assert that the shocks are mutually uncorrelated in market data.
- It does not establish a causal timing convention within a bin.
- It does not validate finite-sample inference or serial-dependence corrections.
- It does not imply that a lower-bias matrix is theoretically admissible or
  economically useful.

Those are later gates. G1 tests only whether these population expressions are
algebraically and numerically correct under their stated data-generating
assumptions.
