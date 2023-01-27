class Channels():
    Verification_Channel = 1068545734842011659
    Hiring_Channel = 1068545665749233786
    For_Hire_Channel = 1068545665749233786


class Post():
    def __init__(self, PostType="Hiring") -> None:
        self.Type = PostType
        self.Title = "Sample Title"
        self.Description = "Sample Description"
        self.Payment = "Robux"
        self.PaymentType = "Upon completion"
        self.Robux = 0.0
        self.USD = 0.0