$(document).ready(function() {
    validate();
    $('input[type=text]').change(validate);
});

function validate() {
    if ($('#dire_player_0').val() &&
        $('#dire_hero_0').val() &&
        $('#dire_player_1').val() &&
        $('#dire_hero_1').val() &&
        $('#dire_player_2').val() &&
        $('#dire_hero_2').val() &&
        $('#dire_player_3').val() &&
        $('#dire_hero_3').val() &&
        $('#dire_player_4').val() &&
        $('#dire_hero_4').val() &&
        $('#radiant_player_0').val() &&
        $('#radiant_hero_0').val() &&
        $('#radiant_player_1').val() &&
        $('#radiant_hero_1').val() &&
        $('#radiant_player_2').val() &&
        $('#radiant_hero_2').val() &&
        $('#radiant_player_3').val() &&
        $('#radiant_hero_3').val() &&
        $('#radiant_player_4').val() &&
        $('#radiant_hero_4').val())
    {
        $('button[type=submit]').attr('disabled', false);
    } else {
        $('button[type=submit]').attr('disabled', true);
    }
}
