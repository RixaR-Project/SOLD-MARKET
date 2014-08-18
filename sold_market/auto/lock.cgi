# $Id: lock.cgi 96 2004-03-12 12:25:28Z mu $

sub Lock
{
	$LOCKED_LEVEL++,return if $LOCKED ne '';
	LockSub();
	DataCommitOrAbort(1); # abort
}

sub UnLock
{
	return if $LOCKED eq '' || --$LOCKED_LEVEL;
	foreach(1..5)
	{
		$LOCKED='',return if rename($LOCKED,$DATA_DIR."/".$LOCK_FILE);
		sleep(1);
	}
	WriteErrorLog("unlock error ".$LOCKED,$LOG_ERROR_FILE);
}

sub LockSub
{
	my $lockfile=$DATA_DIR."/".$LOCK_FILE;
	my $lockfiletime=$lockfile.$NOW_TIME."_".$$."_".$ENV{REMOTE_ADDR};
	$LOCKED=$lockfiletime;
	$LOCKED_LEVEL=1;
	foreach(1..5)
	{
		select(undef,undef,undef,0.5),next if !rename($lockfile,$lockfiletime);
		
		select(undef,undef,undef,0.1); #0.1�b�E�F�C�g�i�d�v�I�j
		return if -e $lockfiletime;
		WriteErrorLog("lock check error",$LOG_ERROR_FILE);
	}
	LockSub2($lockfiletime);
}

sub LockSub2
{
	my($lockfiletime)=@_;
	opendir(LOCKDIR,$DATA_DIR);
	@_=grep(/^$LOCK_FILE/o,readdir(LOCKDIR));
	closedir(LOCKDIR);
	foreach(@_)
	{
		next if !/^$LOCK_FILE(\d+)/ || $NOW_TIME-$1<$AUTO_UNLOCK_TIME || !rename($DATA_DIR."/".$_,$lockfiletime);
		
		select(undef,undef,undef,0.1); #0.1�b�E�F�C�g�i�d�v�I�j
		return if -e $lockfiletime;
		WriteErrorLog("unlock after lock check error",$LOG_ERROR_FILE);
	}
	WriteErrorLog("busy",$LOG_ERROR_FILE);
	$LOCKED='';
	OutErrorBusy();
}

sub RenameAndCheck
{
	foreach(1..5)
	{
		if(rename($_[0],$_[1]))
		{
			select(undef,undef,undef,0.2);
			return if !-e $_[0] && -e $_[1];
		}
		select(undef,undef,undef,0.2);
	}
	WriteErrorLog('rename error '.$_[0]."->".$_[1],$LOG_ERROR_FILE);
	OutError('�ُ폈���ł��B���f���܂����B');
}

sub OpenAndCheck
{
	my $count=5;
	while(!open(OUT,">".$_[0]))
	{
		WriteErrorLog('write mode open error',$LOG_ERROR_FILE),OutError('�ُ폈���ł��B���f���܂����B') if !$count--;
		select(undef,undef,undef,0.2);
	}
}

1;