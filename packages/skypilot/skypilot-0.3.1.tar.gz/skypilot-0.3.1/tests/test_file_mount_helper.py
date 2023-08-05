from sky.backends import backend_utils

make_command = backend_utils.FileMountHelper.make_safe_symlink_command


def test_absolute_paths_needing_sudo():

    file_to_file = {
        '/f': './f',
        '/non_exist_dir/f': './f',
        '/exist_dir/non_exist_dir/f': './f',
    }

    assert False
