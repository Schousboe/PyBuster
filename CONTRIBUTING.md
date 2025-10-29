<div align=center>
<h1> CONTRIBUTING.md - Guide to contribute to <a href="github.com/Schousboe/PyBuster">PyBuster</a> </h1>

<p> Thanks for considering contributing to PyBuster! By contributing, you agree to follow the rules and guidelines below. </p>
</div>

---

<div align=center>
<p>Always love to see your suggestions! We need to make this the best version it can be, and therefore we of course need some people who a down to:</p>
<ul style="display:inline-block; text-align:left;"><strong>
<li> Reporting an issue
<li> Supposing a fix
<li> Proposing new features
</strong>
</ul>

</div>

<br/>

## How to contribute

Pull requests are the best way to get something changed if you wish to do so. PR's are always welcome:

1. **Fork** the repository and create a branch for your feature or bug fix:

   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Make your changes locally.
3. Include tests and update README.md or USAGE.md if needed
4. **Commit** with clear messages:

   ```bash
   git commit -m "scope: Add feature X with Y"
   ```
5. **Push** to your fork and open a pull request describing the change.
6. Keep PRs focused on one issue or feature for easier review.

---

## Coding style

* Python 3.8+ compatible.
* Use **4 spaces** for indentation (no tabs).
* Keep functions small and single-purpose.
* Add clear error messages; avoid silencing exceptions.
* Use descriptive variable names.
* Remember to add a scope (fx. fix:, feat:, docs:, etc.) so our .chglog workflow picks it up

---
<div align=center>
<sub>Thank you for helping improve PyBuster! Every contribution makes it better!</sub>
</div>