from requests.exceptions import HTTPError

from src.core import api
from src.core.filters.date import create_datetime


try:
    # Ask for the prompt date
    entered_date = input("Enter the prompt date (YYYY-MM-DD): ")
    try:
        prompt_date = create_datetime(entered_date)

    # The date was entered in the wrong format
    except ValueError:
        print("Date must be in the format YYYY-MM-DD!")
        input("Press enter to close...")
        raise SystemExit(1)

    # Fetch all Prompts for this date
    available_prompts = api.get("prompt", params={"date": prompt_date})

    # By default, select the first/latest Prompt
    prompt_index = -1

    # There's > 1 recorded Prompt for the day. Ask which should be sent out
    num_of_prompts = len(available_prompts)
    if num_of_prompts >= 2:
        print(
            f"\nThere are {num_of_prompts} Prompts for {prompt_date}. Which would you like to broadcast?"
        )
        for i, prompt in enumerate(available_prompts):
            print(f"[{i + 1}] {prompt['word']}")

        # Ask for a prompt until we get a valid selection
        while True:
            selected_prompt = input("> ")

            # Make sure we have a number input and it's within range
            # This check has the advanage of automatically disallowing
            # a negative index
            if not selected_prompt.isnumeric() or int(selected_prompt) > num_of_prompts:
                print("Please enter a prompt number")
                continue
            break

        # Properly index the selected Prompt
        prompt_index = int(selected_prompt) - 1

    # Send out the broadcast
    api.post(
        "broadcast",
        headers=api.create_auth_token(),
        params={"date": prompt_date, "which": prompt_index},
    )
    print(f"Email broadcast for {prompt_date} successfully sent")

# A broadcast for that day couldn't be sent
except HTTPError:
    print(f"Unable to send email broadcast for {prompt_date}!")
raise SystemExit(0)
