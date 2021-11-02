from flask import Flask, render_template, request


def engine(TEST):
    return render_template(
        'test_editor.html',
        obj=TEST
    )
