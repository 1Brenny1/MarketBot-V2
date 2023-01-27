from discord import *
from discord.ext import commands
from discord.ui import Button, View, Select, modal
import discord

import Posts

class Post(commands.Cog):
    def __init__(self, Client):
        self.Client:commands.Bot
        self.Client = Client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {self.__cog_name__} ready")


    @app_commands.command(name="post",description="Open the marketplace post menu")
    @app_commands.describe()
    async def post(self, ctx: discord.Interaction) -> None:
        view = View()

        PostType = Select(placeholder="Post Type", options=[
            SelectOption(label="Hiring", emoji="📜", description="Make a hiring post"),
            SelectOption(label="For Hire", emoji="📜", description="Make a for hire post"),
        ])

        view.add_item(PostType)
        async def PostType_CallBack(ctx: discord.Interaction):
            CurrentPost = Posts.Post(PostType=PostType.values[0])

            async def UpdatePreview(ctx: discord.Interaction, Payment=None, PaymentType=None, Title=None, Description=None, Robux=None, USD=None, Return=False):
                if Payment is not None:
                    CurrentPost.Payment = Payment
                if PaymentType is not None:
                    CurrentPost.PaymentType = PaymentType

                if Title is not None:
                    if Title != "":
                        CurrentPost.Title = Title
                if Description is not None:
                    if Description != "":
                        CurrentPost.Description = Description
                
                if Robux is not None:
                    if Robux != "":
                        try:
                            CurrentPost.Robux = int(Robux)
                        except:
                            pass
                if USD is not None:
                    if USD != "":
                        try:
                            CurrentPost.USD = float(USD)
                        except:
                            pass
                

                preview = Embed()
                preview.title = CurrentPost.Title
                preview.description = CurrentPost.Description
                preview.set_author(name=ctx.user.name, icon_url=ctx.user.avatar)
                if CurrentPost.Type == "Hiring":
                    if CurrentPost.Payment == "Robux":
                        preview.add_field(name="Payment", value=f"**Robux:** R${CurrentPost.Robux} ({round((CurrentPost.Robux*0.7)/80, 2)} USD)")
                    elif CurrentPost.Payment == "USD":
                       preview.add_field(name="Payment", value=f"**USD:** ${CurrentPost.USD}")
                    elif CurrentPost.Payment == "Both":
                        preview.add_field(name="Payment", value=f"**Robux:** R${CurrentPost.Robux} ({round((CurrentPost.Robux*0.7)/80, 2)} USD)\n**USD:** ${CurrentPost.USD}")
                if CurrentPost.Type == "Hiring":
                    preview.add_field(name="Payment Type", value=CurrentPost.PaymentType)

                if Return:
                    return preview
                await ctx.response.edit_message(embed=preview)

            view = View()

            Payment = Select(placeholder="Payment", options=[
                SelectOption(label="Robux"),
                SelectOption(label="USD"),
                SelectOption(label="Both")
            ])

            async def Payment_CallBack(ctx: discord.Interaction):
                await UpdatePreview(ctx=ctx, Payment=Payment.values[0])
            Payment.callback = Payment_CallBack


            PaymentType = Select(placeholder="Payment Type", options=[
                SelectOption(label="Up front", description="Up front payment."),
                SelectOption(label="Partial up front", description="Partial up front payment."),
                SelectOption(label="Upon completion", description="One time payment."),
                SelectOption(label="Per Task", description="Per task payment.")
            ])

            async def PaymentType_CallBack(ctx: discord.Interaction):
                await UpdatePreview(ctx=ctx, PaymentType=PaymentType.values[0])
            PaymentType.callback = PaymentType_CallBack

            EditInfoBtn = Button(label="Edit Post Info", emoji="⚙", style=discord.ButtonStyle.red)
            EditPaymentBtn = Button(label="Edit Payment Info", emoji="💲", style=discord.ButtonStyle.red)
            view.add_item(EditInfoBtn)
            if CurrentPost.Type == "Hiring":
                view.add_item(EditPaymentBtn)

            async def EditInfo_CallBack(ctx: discord.Interaction):
                InfoModal = modal.Modal(title="Edit Post Info")

                Title = ui.TextInput(label="Post Title", style=discord.TextStyle.short, required=False, placeholder="Sample Title")
                Description = ui.TextInput(label="Post Description", style=discord.TextStyle.long, required=False, placeholder="Sample Description")
                InfoModal.add_item(Title)
                InfoModal.add_item(Description)

                async def InfoModal_CallBack(ctx: discord.Interaction):
                    await UpdatePreview(ctx, Title=Title.value, Description=Description.value)
                InfoModal.on_submit = InfoModal_CallBack

                await ctx.response.send_modal(InfoModal)

            EditInfoBtn.callback = EditInfo_CallBack

            async def EditPayment_CallBack(ctx: discord.Interaction):
                PaymentModal = modal.Modal(title="Edit Payment Info")

                Robux = ui.TextInput(label="Robux (Without Prefix)", style=discord.TextStyle.short, required=False, placeholder="800")
                USD = ui.TextInput(label="USD (Without Prefix)", style=discord.TextStyle.short, required=False, placeholder="10")
                PaymentModal.add_item(Robux)
                PaymentModal.add_item(USD)

                async def PaymentModal_CallBack(ctx: discord.Interaction):
                    await UpdatePreview(ctx, Robux=Robux.value, USD=USD.value)
                PaymentModal.on_submit = PaymentModal_CallBack

                await ctx.response.send_modal(PaymentModal)
            
            EditPaymentBtn.callback = EditPayment_CallBack

            if CurrentPost.Type == "Hiring":
                view.add_item(Payment)
                view.add_item(PaymentType)
                
            SubmitBtn = Button(label="Submit for review", emoji="✅", style=discord.ButtonStyle.green, row=4)
            view.add_item(SubmitBtn)

            async def Submit_CallBack(ctx: discord.Interaction):
                Post_Verify = self.Client.get_channel(Posts.Channels.Verification_Channel)

                view = View()

                Accept = Button(label="Accept Post", emoji="✅", style=discord.ButtonStyle.green)
                Reject = Button(label="Reject Post", emoji="✖", style=discord.ButtonStyle.red)
                view.add_item(Accept)
                view.add_item(Reject)

                async def Accept_CallBack(ctx: discord.Interaction):
                    if CurrentPost.Type == "Hiring":
                        PostChnl = self.Client.get_channel(Posts.Channels.Hiring_Channel)
                    else:
                        PostChnl = self.Client.get_channel(Posts.Channels.For_Hire_Channel)
                    embed:Embed = ctx.message.embeds[0]
                    embed.set_footer(text=f"Accepted by {ctx.user.name}")
                    await PostChnl.send(embed=embed)

                    await ctx.message.delete()
                Accept.callback = Accept_CallBack

                async def Reject_CallBack(ctx: discord.Interaction):
                    await ctx.message.delete()
                Reject.callback = Reject_CallBack

                await Post_Verify.send(embed=ctx.message.embeds[0], view=view)
                await ctx.response.edit_message(content="Post sent for verification", view=None, embed=None)


            SubmitBtn.callback = Submit_CallBack

            DeleteBtn = Button(label="Delete Post", emoji="❌", style=discord.ButtonStyle.gray, row=4)
            view.add_item(DeleteBtn)

            async def Delete_CallBack(ctx: discord.Interaction):
                await ctx.response.edit_message(content="Post Deleted", view=None, embed=None)
            DeleteBtn.callback = Delete_CallBack

            await ctx.response.edit_message(view=view, embed= await UpdatePreview(ctx=ctx, Return=True))

        PostType.callback = PostType_CallBack

        await ctx.response.send_message(view=view, ephemeral=True)

async def setup(Client):
    await Client.add_cog(Post(Client))