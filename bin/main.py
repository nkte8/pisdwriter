#!/usr/bin/python3 -B
import jinja2_writter

if __name__ == "__main__":
    template_files={
        "network-config",
        "user-data"
    }
    for template_file in template_files:
        jinja2_writter.write_config(template_file)
