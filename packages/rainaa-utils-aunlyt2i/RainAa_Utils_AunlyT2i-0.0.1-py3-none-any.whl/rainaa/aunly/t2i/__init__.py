import asyncio
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from .strings import get_cut_str
from rainaa.res.fonts import sarasa_mono_sc_semibold_ttf

font = ImageFont.truetype(sarasa_mono_sc_semibold_ttf(), size=20)

async def text2image(text: str, cut=64) -> bytes:
    return await asyncio.to_thread(_create_image, text, cut)


def _create_image(text: str, cut: int) -> bytes:
    cut_str = "\n".join(get_cut_str(text, cut))
    textx, texty = font.getsize_multiline(cut_str)
    image = Image.new("RGB", (textx + 40, texty + 40), (235, 235, 235))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), cut_str, font=font, fill=(31, 31, 33))
    imageio = BytesIO()
    image.save(
        imageio,
        format="JPEG",
        quality=90,
        subsampling=2,
        qtables="web_high",
    )
    return imageio.getvalue()


async def rich_text2image(data: str):
    from io import BytesIO
    from minidynamicrender.DynConfig import ConfigInit
    from minidynamicrender.DynText import DynTextRender
    from dynamicadaptor.Content import Text, RichTextDetail
    import importlib.resources as pkg_res
    import minidynamicrender as res
    from rainaa.res.fonts import HarmonyOS_Sans_SC_Medium_Woff2, nte_ttf, sarasa_mono_sc_bold_ttf

    with pkg_res.path(res,"Core.py") as p:
        data_path = str(p).removesuffix("Core.py")
    # 绝对不允许拉在我的机器人运行目录里 😡
    config = ConfigInit(
        data_path=data_path, # 塞回去
        font_path={
            "text": HarmonyOS_Sans_SC_Medium_Woff2(),
            "extra_text": sarasa_mono_sc_bold_ttf(),
            "emoji": nte_ttf(),
        },
    )
    if config.dyn_color and config.dyn_font and config.dy_size:
        render = DynTextRender(
            config.static_path, config.dyn_color, config.dyn_font, config.dy_size
        )
        image = await render.run(
            Text(
                text=data,
                topic=None,
                rich_text_nodes=[
                    RichTextDetail(
                        type="RICH_TEXT_NODE_TYPE_TEXT", text=data, orig_text=data, emoji=None
                    )
                ],
            )
        )
        if image:
            bio = BytesIO()
            image.convert("RGB").save(bio, "jpeg", optimize=True)
            return bio.getvalue()


async def browser_text2image(data: str):
    from graiax.text2img.playwright import convert_md
    from graiax.playwright.interface import PlaywrightContext
    from graiax.text2img.playwright.renderer import BuiltinCSS

    from launart import Launart


    browser_context = Launart.current().get_interface(PlaywrightContext).context
    page = await browser_context.new_page()
    await page.set_viewport_size({"width": 400, "height": 100})
    md = convert_md(data)
    css = "\n".join(BuiltinCSS.one_dark.value)
    await page.set_content(
        '<html><head><meta name="viewport" content="width=device-width,initial-scale=1.0">'
        f"<style>{css}</style></head><body>{md}<body></html>"
    )
    return await page.screenshot(full_page=True, type="jpeg", quality=95)