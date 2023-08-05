import importlib.resources as pkg_resources
import rainaa.res.fonts._fonts as _fonts


def HarmonyOS_Sans_SC_Medium_Woff2():
    with pkg_resources.path(_fonts, "HarmonyOS_Sans_SC_Medium.woff2") as f:
        return str(f)


def nte_ttf():
    with pkg_resources.path(_fonts, "nte.ttf") as f:
        return str(f)


def vanfont_ttf():
    with pkg_resources.path(_fonts, "vanfont.ttf") as f:
        return str(f)


def sarasa_mono_sc_bold_ttf():
    with pkg_resources.path(_fonts, "sarasa-mono-sc-bold.ttf") as f:
        return str(f)


def sarasa_mono_sc_semibold_ttf():
    with pkg_resources.path(_fonts, "sarasa-mono-sc-semibold.ttf") as f:
        return str(f)
