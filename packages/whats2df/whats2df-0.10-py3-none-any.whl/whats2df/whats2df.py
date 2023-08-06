import os.path
import subprocess
import sys
import pandas as pd
from a_pandas_ex_read_sql import read_sqlite
from downloadunzip import download_and_extract
from touchtouch import touch
from search_in_syspath import search_in_syspath
from hackyargparser import add_sysargv


def decrypt_database(key, file, output):
    decryptexe = os.path.normpath(
        search_in_syspath(filename="decrypt14_15.exe", isregex=False)[0]
    )
    file = os.path.normpath(file)
    output = os.path.normpath(output)
    touch(output)
    subprocess.run([decryptexe, key, file, output])


def download_and_copy_dlls(
    sqlzip="https://www.sqlite.org/2023/sqlite-dll-win64-x64-3420000.zip",
):
    folder = "\\".join((sys.executable.split("\\")[:-1] + ["DLLs"]))
    try:
        download_and_extract(
            url=sqlzip,
            folder=folder,
        )
    except Exception as fe:
        print(fe)


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    dtypes = [
        ("_id_x", "uint32"),
        ("chat_row_id", "uint16"),
        ("from_me", "uint8"),
        ("key_id", "string"),
        ("sender_jid_row_id", "uint16"),
        ("status", "uint8"),
        ("broadcast", "uint8"),
        ("recipient_count", "uint16"),
        ("participant_hash", "category"),
        ("origination_flags", "uint16"),
        ("origin", "uint8"),
        ("timestamp", "Int64"),
        ("received_timestamp", "uint64"),
        ("receipt_server_timestamp", "float64"),
        ("message_type", "uint8"),
        ("text_data", "string"),
        ("starred", "uint8"),
        ("lookup_tables", "uint8"),
        ("sort_id", "uint32"),
        ("message_add_on_flags", "uint8"),
        ("_id_y", "Int64"),
        ("key_remote_jid", "category"),
        ("remote_resource", "category"),
        ("receipt_device_timestamp", "Int64"),
        ("read_device_timestamp", "Int64"),
        ("played_device_timestamp", "Int64"),
        ("user_id", "uint16"),
        ("_id", "Int64"),
        ("user", "category"),
        ("server", "category"),
        ("agent", "uint8"),
        ("type", "uint8"),
        ("raw_string", "category"),
        ("device", "Int64"),
        ("conversation__id", "uint16"),
        ("conversation_jid_row_id", "uint16"),
        ("conversation_hidden", "uint8"),
        ("conversation_subject", "category"),
        ("conversation_display_message_row_id", "Int64"),
        ("conversation_last_message_row_id", "Int64"),
        ("conversation_last_read_message_row_id", "Int64"),
        ("conversation_last_read_receipt_sent_message_row_id", "Int64"),
        ("conversation_last_important_message_row_id", "Int64"),
        ("conversation_archived", "Int64"),
        ("conversation_sort_timestamp", "Int64"),
        ("conversation_mod_tag", "Int64"),
        ("conversation_gen", "Int64"),
        ("conversation_unseen_earliest_message_received_time", "Int64"),
        ("conversation_unseen_message_count", "Int64"),
        ("conversation_unseen_missed_calls_count", "Int64"),
        ("conversation_unseen_row_count", "Int64"),
        ("conversation_plaintext_disabled", "Int64"),
        ("conversation_vcard_ui_dismissed", "Int64"),
        ("conversation_change_number_notified_message_row_id", "Int64"),
        ("conversation_show_group_description", "Int64"),
        ("conversation_ephemeral_expiration", "Int64"),
        ("conversation_last_read_ephemeral_message_row_id", "Int64"),
        ("conversation_ephemeral_setting_timestamp", "Int64"),
        ("conversation_unseen_important_message_count", "uint8"),
        ("conversation_ephemeral_disappearing_messages_initiator", "Int64"),
        ("conversation_group_type", "uint8"),
        ("conversation_last_message_reaction_row_id", "Int64"),
        ("conversation_last_seen_message_reaction_row_id", "Int64"),
        ("conversation_unseen_message_reaction_count", "Int64"),
        ("conversation_growth_lock_level", "Int64"),
        ("conversation_growth_lock_expiration_ts", "Int64"),
        ("conversation_display_message_sort_id", "Int64"),
        ("conversation_last_message_sort_id", "Int64"),
        ("conversation_last_read_receipt_sent_message_sort_id", "Int64"),
        ("message_forwarded", "bool"),
        ("message_template_message_row_id", "Int64"),
        ("message_template_content_text_data", "category"),
        ("message_template_footer_text_data", "category"),
        ("message_template_csat_trigger_expiration_ts", "Int64"),
        ("message_template_button__id", "Int64"),
        ("message_template_button_message_row_id", "Int64"),
        ("message_template_button_text_data", "category"),
        ("message_template_button_extra_data", "category"),
        ("message_template_button_button_type", "Int64"),
        ("message_template_button_used", "Int64"),
        ("message_template_button_selected_index", "Int64"),
        ("message_template_button_otp_button_type", "Int64"),
        ("message_location_message_row_id", "Int64"),
        ("message_location_chat_row_id", "Int64"),
        ("message_location_place_name", "category"),
        ("message_location_place_address", "category"),
        ("message_location_url", "category"),
        ("message_location_live_location_share_duration", "Int64"),
        ("message_location_live_location_sequence_number", "Int64"),
        ("message_location_live_location_final_timestamp", "Int64"),
        ("message_location_map_download_status", "Int64"),
        ("message_quoted_location_message_row_id", "Int64"),
        ("message_quoted_location_latitude", "Float64"),
        ("message_quoted_location_place_name", "category"),
        ("message_quoted_location_place_address", "category"),
        ("message_quoted_location_url", "category"),
        ("message_mentions__id", "Int64"),
        ("message_mentions_message_row_id", "Int64"),
        ("message_mentions_jid_row_id", "Int64"),
        ("message_media_message_row_id", "Int64"),
        ("message_media_chat_row_id", "Int64"),
        ("message_media_autotransfer_retry_enabled", "Int64"),
        ("message_media_multicast_id", "category"),
        ("message_media_media_job_uuid", "category"),
        ("message_media_transferred", "Int64"),
        ("message_media_transcoded", "Int64"),
        ("message_media_file_path", "category"),
        ("message_media_file_size", "Int64"),
        ("message_media_suspicious_content", "Int64"),
        ("message_media_trim_from", "Int64"),
        ("message_media_trim_to", "Int64"),
        ("message_media_media_key_timestamp", "Int64"),
        ("message_media_width", "Int64"),
        ("message_media_height", "Int64"),
        ("message_media_has_streaming_sidecar", "Int64"),
        ("message_media_gif_attribution", "Int64"),
        ("message_media_direct_path", "category"),
        ("message_media_first_scan_length", "Int64"),
        ("message_media_message_url", "category"),
        ("message_media_mime_type", "category"),
        ("message_media_file_length", "Int64"),
        ("message_media_media_name", "category"),
        ("message_media_file_hash", "category"),
        ("message_media_media_duration", "Int64"),
        ("message_media_page_count", "Int64"),
        ("message_media_enc_file_hash", "category"),
        ("message_media_partial_media_hash", "category"),
        ("message_media_partial_media_enc_hash", "category"),
        ("message_media_is_animated_sticker", "Int64"),
        ("message_media_original_file_hash", "category"),
        ("message_media_mute_video", "Int64"),
        ("message_vcard__id", "Int64"),
        ("message_vcard_message_row_id", "Int64"),
        ("message_vcard_vcard", "category"),
        ("message_vcard_jid__id", "Int64"),
        ("message_vcard_jid_vcard_jid_row_id", "Int64"),
        ("message_vcard_jid_vcard_row_id", "Int64"),
        ("message_vcard_jid_message_row_id", "Int64"),
        ("message_streaming_sidecar_message_row_id", "Int64"),
        ("message_streaming_sidecar_timestamp", "Int64"),
        ("message_quoted_media_message_row_id", "Int64"),
        ("message_quoted_media_media_job_uuid", "category"),
        ("message_quoted_media_transferred", "Int64"),
        ("message_quoted_media_file_path", "category"),
        ("message_quoted_media_file_size", "Int64"),
        ("message_quoted_media_media_key_timestamp", "Int64"),
        ("message_quoted_media_width", "Int64"),
        ("message_quoted_media_height", "Int64"),
        ("message_quoted_media_direct_path", "category"),
        ("message_quoted_media_message_url", "category"),
        ("message_quoted_media_mime_type", "category"),
        ("message_quoted_media_file_length", "Int64"),
        ("message_quoted_media_media_name", "category"),
        ("message_quoted_media_file_hash", "category"),
        ("message_quoted_media_media_duration", "Int64"),
        ("message_quoted_media_page_count", "Int64"),
        ("message_quoted_media_enc_file_hash", "category"),
        ("message_quoted_mentions__id", "Int64"),
        ("message_quoted_mentions_message_row_id", "Int64"),
        ("message_quoted_mentions_jid_row_id", "Int64"),
        ("message_thumbnail_message_row_id", "Int64"),
        ("message_link__id", "Int64"),
        ("message_link_chat_row_id", "Int64"),
        ("message_link_message_row_id", "Int64"),
        ("message_link_link_index", "Int64"),
        ("message_quoted_vcard__id", "Int64"),
        ("message_quoted_vcard_message_row_id", "Int64"),
        ("message_quoted_vcard_vcard", "category"),
        ("message_text_message_row_id", "Int64"),
        ("message_text_description", "category"),
        ("message_text_page_title", "category"),
        ("message_text_url", "category"),
        ("message_text_font_style", "Int64"),
        ("message_text_preview_type", "Int64"),
        ("message_text_invite_link_group_type", "Int64"),
        ("message_quoted_text_message_row_id", "Int64"),
        ("message_send_count_message_row_id", "Int64"),
        ("message_send_count_send_count", "Int64"),
        ("receipt_device__id", "Int64"),
        ("receipt_device_message_row_id", "Int64"),
        ("receipt_device_receipt_device_jid_row_id", "Int64"),
        ("receipt_device_receipt_device_timestamp", "Int64"),
        ("receipt_device_primary_device_version", "Int64"),
        ("message_system_message_row_id", "Int64"),
        ("message_system_action_type", "Int64"),
        ("message_system_group_message_row_id", "Int64"),
        ("message_system_group_is_me_joined", "Int64"),
        ("message_system_value_change_message_row_id", "Int64"),
        ("message_system_value_change_old_data", "category"),
        ("message_system_number_change_message_row_id", "Int64"),
        ("message_system_number_change_old_jid_row_id", "Int64"),
        ("message_system_number_change_new_jid_row_id", "Int64"),
        ("message_system_photo_change_message_row_id", "Int64"),
        ("message_system_photo_change_new_photo_id", "category"),
        ("message_system_chat_participant_message_row_id", "Int64"),
        ("message_system_chat_participant_user_jid_row_id", "Int64"),
        ("receipt_user__id", "Int64"),
        ("receipt_user_message_row_id", "Int64"),
        ("receipt_user_receipt_user_jid_row_id", "Int64"),
        ("receipt_user_read_timestamp", "Int64"),
        ("receipt_user_played_timestamp", "Int64"),
        ("message_revoked_message_row_id", "Int64"),
        ("message_revoked_revoked_key_id", "category"),
        ("message_revoked_admin_jid_row_id", "Int64"),
        ("messages_hydrated_four_row_template_message_row_id", "Int64"),
        ("message_ephemeral_setting_message_row_id", "Int64"),
        ("message_ephemeral_setting_setting_duration", "Int64"),
        ("message_ephemeral_setting_setting_reason", "Int64"),
        ("message_view_once_media_message_row_id", "Int64"),
        ("message_view_once_media_state", "Int64"),
        ("mms_thumbnail_metadata_message_row_id", "Int64"),
        ("mms_thumbnail_metadata_direct_path", "category"),
        ("mms_thumbnail_metadata_media_key_timestamp", "Int64"),
        ("mms_thumbnail_metadata_enc_thumb_hash", "category"),
        ("mms_thumbnail_metadata_thumb_hash", "category"),
        ("mms_thumbnail_metadata_thumb_width", "Int64"),
        ("mms_thumbnail_metadata_thumb_height", "Int64"),
        ("mms_thumbnail_metadata_transferred", "Int64"),
        ("mms_thumbnail_metadata_insert_timestamp", "Int64"),
        ("message_system_initial_privacy_provider_message_row_id", "Int64"),
        ("message_system_initial_privacy_provider_privacy_provider", "Int64"),
        ("message_system_initial_privacy_provider_biz_state_id", "Int64"),
        ("message_privacy_state_message_row_id", "Int64"),
        ("message_privacy_state_host_storage", "Int64"),
        ("message_privacy_state_actual_actors", "Int64"),
        ("message_privacy_state_privacy_mode_ts", "Int64"),
        ("message_system_business_state_message_row_id", "Int64"),
        ("message_system_business_state_privacy_message_type", "Int64"),
        ("message_system_business_state_business_name", "category"),
        ("message_ephemeral_message_row_id", "Int64"),
        ("message_ephemeral_duration", "Int64"),
        ("message_ephemeral_expire_timestamp", "Int64"),
        ("message_ephemeral_keep_in_chat", "Int64"),
        ("played_self_receipt_message_row_id", "Int64"),
        ("played_self_receipt_to_jid_row_id", "Int64"),
        ("played_self_receipt_message_id", "category"),
        ("message_system_linked_group_call_message_row_id", "Int64"),
        ("message_system_linked_group_call_call_id", "category"),
        ("message_system_linked_group_call_is_video_call", "Int64"),
        ("audio_data_message_row_id", "Int64"),
    ]
    for dty in dtypes:
        try:
            df[dty[0]] = df[dty[0]].astype(dty[1])
            print(f"{dty[0]} -> {dty[1]}                    ", end="\r")
        except Exception as fe:
            continue
    return df


def convert_whatsapp_to_df(
    sql_database: str,
    databases_to_add: tuple = (
        "message_template",
        "message_template_button",
        "message_location",
        "message_quoted_location",
        "message_mentions",
        "message_media",
        "message_vcard",
        "message_vcard_jid",
        "message_streaming_sidecar",
        "message_quoted_media",
        "message_quoted",
        "message_quoted_mentions",
        "message_thumbnail",
        "message_link",
        "message_quoted_vcard",
        "message_text",
        "message_quoted_text",
        "message_send_count",
        "receipt_device",
        "message_system",
        "message_system_group",
        "message_system_value_change",
        "message_system_number_change",
        "message_system_photo_change",
        "message_system_chat_participant",
        "receipt_user",
        "message_revoked",
        "messages_hydrated_four_row_template",
        "message_system_block_contact",
        "message_ephemeral_setting",
        "message_view_once_media",
        "mms_thumbnail_metadata",
        "message_system_initial_privacy_provider",
        "message_privacy_state",
        "message_system_business_state",
        "message_ephemeral",
        "played_self_receipt",
        "message_system_linked_group_call",
        "audio_data",
    ),
    optimize_dtypes: bool = True,
) -> pd.DataFrame:
    """
    Parameters:
        sql_database: str
            The file path to your decrypted SQL Database
        databases_to_add: tuple
            The SQL tables to include in the output DataFrame
            default = (
            "message_template",
            "message_template_button",
            "message_location",
            "message_quoted_location",
            "message_mentions",
            "message_media",
            "message_vcard",
            "message_vcard_jid",
            "message_streaming_sidecar",
            "message_quoted_media",
            "message_quoted",
            "message_quoted_mentions",
            "message_thumbnail",
            "message_link",
            "message_quoted_vcard",
            "message_text",
            "message_quoted_text",
            "message_send_count",
            "receipt_device",
            "message_system",
            "message_system_group",
            "message_system_value_change",
            "message_system_number_change",
            "message_system_photo_change",
            "message_system_chat_participant",
            "receipt_user",
            "message_revoked",
            "messages_hydrated_four_row_template",
            "message_system_block_contact",
            "message_ephemeral_setting",
            "message_view_once_media",
            "mms_thumbnail_metadata",
            "message_system_initial_privacy_provider",
            "message_privacy_state",
            "message_system_business_state",
            "message_ephemeral",
            "played_self_receipt",
            "message_system_linked_group_call",
            "audio_data",
            )
        optimize_dtypes:bool
            Optimize dtypes at the end of the conversion to save memory
            default = True
    Returns
        df: pd.DataFrame
    """

    def extract_extra_info(rowtoadd):
        toadd = df2[rowtoadd].loc[df2[rowtoadd].message_row_id.isin(df._id_x)].copy()
        toadd.columns = [f"{rowtoadd}_{x}" for x in toadd.columns]
        lenda = len(toadd)
        print(rowtoadd, lenda)
        for _ in range(len(toadd) - 1):
            print(f"{_} / {lenda}", end="\r")
            filtax = df._id_x == toadd[f"{rowtoadd}_message_row_id"].iloc[_]
            filt1 = df.loc[filtax]
            addings = toadd.iloc[_ : _ + 1].loc[
                toadd.iloc[_ : _ + 1].index.repeat(len(filt1))
            ]
            addings.index = filt1.index.__array__().copy()
            df.loc[filtax, addings.columns] = addings.copy()

    output = sql_database
    df2 = read_sqlite(output)
    df_ = pd.merge(
        df2["message"], df2["receipts"], right_on="key_id", left_on="key_id", how="left"
    ).drop_duplicates()
    df_ = (
        df_.loc[df_.chat_row_id > 0]
        .sort_values(by="chat_row_id")
        .reset_index(drop=True)
        .copy()
    )
    df_["phone_number"] = pd.NA

    stillna2 = df_.loc[df_.phone_number.isna()]

    for name, group in stillna2.groupby("chat_row_id"):
        print(name, end="\r")
        lookingfor = group.chat_row_id.iloc[0]
        df2xa = df2["chat"].loc[df2["chat"]["_id"] == lookingfor]
        lookinforuser = df2xa.jid_row_id.iloc[0]
        dausa = df2["jid"].loc[df2["jid"]["_id"] == lookinforuser].copy()
        newdfa3 = dausa.user.str.extractall(
            r"(?P<phone_number>^\d+)(?P<group>-\d+)?"
        ).copy()
        newdfa3 = (
            newdfa3.reset_index()
            .drop_duplicates(subset="level_0")
            .set_index("level_0")
            .drop(columns="match")
            .copy()
        )
        dausa.loc[newdfa3.index, "phone_number"] = newdfa3.phone_number.copy()
        dausa.loc[newdfa3.index, "group"] = newdfa3.group.str.strip("-").copy()

        dausa.loc[newdfa3.index, "phone_number"] = newdfa3.phone_number.copy()
        dausa.loc[newdfa3.index, "group"] = newdfa3.group.str.strip("-").copy()
        df_.loc[group.index, "user_id"] = lookinforuser
        for cola in dausa.columns:
            df_.loc[group.index, cola] = dausa[cola].iloc[0]

    missedcalls = df2["missed_call_logs"].loc[
        df2["missed_call_logs"].timestamp.isin(df_.timestamp)
    ]
    dfindi = df_.loc[df_.timestamp.isin(missedcalls.timestamp)]
    callindex = dfindi.index
    for col in missedcalls.columns:
        df_.loc[callindex, col] = missedcalls[col].copy()

    df = df_.copy()
    del df_
    df41 = df2["chat"].copy()
    df41.columns = [f"conversation_{x}" for x in df41.columns]
    df = (
        pd.merge(
            df, df41, left_on="chat_row_id", right_on="conversation__id", how="outer"
        )
    ).copy()
    del df41

    gid = df.loc[(~df.group.isna()) & (df.recipient_count > 1)].sender_jid_row_id
    toadd = df2["jid"].loc[df2["jid"]["_id"].isin(gid)].copy()
    prefilter = (~df.group.isna()) & (df.recipient_count > 1)
    toadd.columns = [
        "user_id",
        "user",
        "server",
        "agent",
        "type",
        "raw_string",
        "device",
    ]
    toaddfilt = [
        "phone_number",
        "user_id",
        "user",
        "server",
        "agent",
        "type",
        "raw_string",
        "device",
    ]
    for _ in range(len(toadd) - 1):
        print(_, end="\r")
        filt1 = df.loc[
            (prefilter & (df.sender_jid_row_id == toadd.user_id.iloc[_])), toaddfilt
        ]

        addings = toadd.iloc[_ : _ + 1].loc[
            toadd.iloc[_ : _ + 1].index.repeat(len(filt1))
        ]
        addings.insert(0, "phone_number", addings.user.iloc[0].split("-")[0])
        addings.index = filt1.index.__array__().copy()
        df.loc[
            (prefilter & (df.sender_jid_row_id == toadd.user_id.iloc[_])), toaddfilt
        ] = addings.copy()

    df.loc[:, "message_forwarded"] = False
    df.loc[
        df._id_x.isin(df2["message_forwarded"].message_row_id), "message_forwarded"
    ] = True

    del gid
    del toadd
    del prefilter

    for rowtoadd in databases_to_add:
        try:
            extract_extra_info(rowtoadd)
        except Exception as das:
            continue

    df = df.loc[~df.chat_row_id.isna()].reset_index(drop=True).copy()
    del df2
    if optimize_dtypes:
        df = convert_dtypes(df)
    return df


def pd_add_whatsapp_to_df():
    pd.Q_whatsapp_to_df = convert_whatsapp_to_df


@add_sysargv
def convert_whatsapp2pandas(
    decryptkey: str | None = None,
    encrypted_db: str | None = None,
    decrypted_db: str | None = None,
    output_df: str | None = None,
    download_sql_dll: int | bool = 1,
):
    if download_sql_dll:
        download_and_copy_dlls(
            sqlzip="https://www.sqlite.org/2023/sqlite-dll-win64-x64-3420000.zip"
        )
    decrypt_database(decryptkey, encrypted_db, decrypted_db)
    df = convert_whatsapp_to_df(decrypted_db)
    touch(output_df)
    df.to_pickle(output_df)


if __name__ == "__main__":
    convert_whatsapp2pandas()
