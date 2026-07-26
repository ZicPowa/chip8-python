# chip8-python
![Static Badge](https://img.shields.io/badge/License-MIT-blue)
A Chip8 emulator written in Python

![Screenshot of Pong game](docs/screenshots/pong.png) ![Static Badge](https://img.shields.io/badge/Version-1.0.0-green)

## Quick Start
- Install `pip install -r requirements.txt`
- Put your ROM in a folder `test_roms` and update the path in main.py
- Run `python src/main.py`

## Future Plans

- [ ] Rewrite cpu dispatch to use nested match rather than if/elif/else for performance
- [ ] GUI to select games
- [ ] Save state feature
- [ ] CHIP 48 Support
- [ ] SUPER-CHIP Support
- [ ] Debug mode (manually step through each cpu execution)
- [ ] Configurable colour themes
- [ ] Rust rewrite (likely in a companion repo)

## References and Credits

Thank you to: 
- Cowgod for his technical reference
- Timendus and corax89 for their test roms. 

## License

MIT (see LICENSE)

