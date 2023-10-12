from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import emailpassword, session
from supertokens_python.recipe.thirdparty.provider import ProviderInput, ProviderConfig, ProviderClientConfig
from supertokens_python.recipe import thirdpartyemailpassword

init(
    app_info=InputAppInfo(
        app_name="goom",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        api_base_path="/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        # https://try.supertokens.com is for demo purposes. Replace this with the address of your core instance (sign up on supertokens.com), or self host a core.
        connection_uri="http://localhost:3567",
        # api_key=<API_KEY(if configured)>
    ),
    framework='django',
    recipe_list=[
        session.init(), # initializes session features
        thirdpartyemailpassword.init(
            providers=[
                # We have provided you with development keys which you can use for testing.
                # IMPORTANT: Please replace them with your own OAuth keys for production use.
                ProviderInput(
                    config=ProviderConfig(
                        third_party_id="google",
                        clients=[
                            ProviderClientConfig(
                                client_id="610752118786-r4i3uvktg4857lf36rn1dsprfljuuebs.apps.googleusercontent.com",
                                client_secret="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",
                            ),
                        ],
                    ),
                ),
            ]
        )
    ],
    mode='asgi' # use wsgi if you are running django server in sync mode
)